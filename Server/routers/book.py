from fastapi import APIRouter, Depends, HTTPException, status, Body, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .. import models, Schemas, Oauth
from ..database import get_db

router = APIRouter(prefix="/books", tags=["Books"])


def get_or_create_book(
    db: Session, 
    google_book_id: str, 
    title: str | None = None, 
    authors: list[str] | None = None,  
    thumbnail: str | None = None
):
    book = db.query(models.Book).filter(
        models.Book.google_book_id == google_book_id
    ).one_or_none()
    
    if book:
        updated = False
        if title and book.title != title:
            book.title = title
            updated = True
        if authors and book.authors != authors:
            book.authors = authors  
            updated = True
        if thumbnail and book.thumbnail != thumbnail:
            book.thumbnail = thumbnail
            updated = True
        if updated:
            db.add(book)
            db.commit()
            db.refresh(book)
        return book

    book = models.Book(
        google_book_id=google_book_id,
        title=title,
        authors=authors,  
        thumbnail=thumbnail
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.post("/vote", response_model=Schemas.BookVoteResponse)
def vote_book(
    payload: Schemas.BookVoteAction = Body(...),
    db: Session = Depends(get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):
    
    user_record = db.query(models.Login).filter(models.Login.username == current_user.username).one_or_none()
    if not user_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User record not found")

    book = get_or_create_book(db, payload.google_book_id, payload.title, payload.authors, payload.thumbnail)

    if payload.action == "unlike":
        like = db.query(models.Like).filter(models.Like.user_id == user_record.id, models.Like.book_id == book.id).one_or_none()
        if like:
            db.delete(like)
            db.commit()
    else:
        like = models.Like(user_id=user_record.id, book_id=book.id)
        db.add(like)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()  

    likes = db.query(models.Like).filter(models.Like.book_id == book.id).all()
    users = [{"username": l.user.username, "name": l.user.Name} for l in likes]  

    return Schemas.BookVoteResponse(
        google_book_id=book.google_book_id,
        title=book.title,
        thumbnail=book.thumbnail,
        vote_count=len(likes),
        users=users
    )


@router.get("/{google_book_id}/votes", response_model=Schemas.BookVoteResponse)
def get_book_votes(google_book_id: str = Path(...), db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.google_book_id == google_book_id).one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    likes = db.query(models.Like).filter(models.Like.book_id == book.id).all()
    users = [{"username": l.user.username, "name": l.user.Name} for l in likes]

    return Schemas.BookVoteResponse(
        google_book_id=book.google_book_id,
        title=book.title,
        thumbnail=book.thumbnail,
        vote_count=len(likes),
        users=users
    )

@router.get("/user/{username}/votes", response_model=list[Schemas.BookVoteResponse])
def get_user_votes(username: str = Path(...), db: Session = Depends(get_db), current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser)):

    if current_user.username != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to view other user's votes")

    user_record = db.query(models.Login).filter(models.Login.username == username).one_or_none()
    if not user_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    likes = db.query(models.Like).filter(models.Like.user_id == user_record.id).all()
    results = []
    for l in likes:
        book = l.book
        all_likes = db.query(models.Like).filter(models.Like.book_id == book.id).all()
        users = [{"username": x.user.username, "name": x.user.Name} for x in all_likes]
        results.append(Schemas.BookVoteResponse(
            google_book_id=book.google_book_id,
            title=book.title,
            thumbnail=book.thumbnail,
            vote_count=len(all_likes),
            users=users
        ))
    return results
