# routers/google_books.py
import os
import requests
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Optional
from sqlalchemy.orm import Session

from .. import models, Schemas, Oauth
from ..database import get_db

router = APIRouter(prefix="/google", tags=["GoogleBooks"])

GOOGLE_BOOKS_BASE = "https://www.googleapis.com/books/v1/volumes"
GOOGLE_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")  

def google_books_request(params: dict) -> dict:

    if GOOGLE_API_KEY:
        params["key"] = GOOGLE_API_KEY
    try:
        r = requests.get(GOOGLE_BOOKS_BASE, params=params, timeout=5)
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=f"Google Books request failed: {str(e)}"
        )
    return r.json()


def extract_book_summary(item: dict, db: Session, current_user_id: Optional[int] = None) -> dict:

    info = item.get("volumeInfo", {})
    image_links = info.get("imageLinks", {}) or {}
    google_book_id = item.get("id")
    
    authors_list = info.get("authors") or []
    
    book_in_db = db.query(models.Book).filter(
        models.Book.google_book_id == google_book_id
    ).first()
    
    is_liked = False
    vote_count = 0
    
    if book_in_db:
        vote_count = db.query(models.Like).filter(
            models.Like.book_id == book_in_db.id
        ).count()
        
        if current_user_id:
            is_liked = db.query(models.Like).filter(
                models.Like.book_id == book_in_db.id,
                models.Like.user_id == current_user_id
            ).first() is not None
    
    return {
        "google_book_id": google_book_id,
        "title": info.get("title"),
        "authors": authors_list,
        "description": info.get("description"),
        "thumbnail": image_links.get("thumbnail") or image_links.get("smallThumbnail"),
        "publishedDate": info.get("publishedDate"),
        "is_liked": is_liked,
        "vote_count": vote_count,
    }


@router.get("/search")
def search_books(
    q: str = Query(..., min_length=1),
    max_results: int = Query(10, le=40),
    db: Session = Depends(get_db),
):
    
    params = {"q": q, "maxResults": max_results}
    raw = google_books_request(params)
    items = raw.get("items", [])
    
    return [extract_book_summary(it, db, None) for it in items]


@router.get("/books/{google_book_id}")
def get_book_detail(
    google_book_id: str = Path(...),
    db: Session = Depends(get_db),
):
   
    raw = google_books_request({"q": google_book_id})
    items = raw.get("items") or []
    
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found in Google Books"
        )
    
    return extract_book_summary(items[0], db, None)


@router.get("/liked")
def get_liked_books(
    db: Session = Depends(get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser)
):
    """Get all books the current user has liked."""
    user_record = db.query(models.Login).filter(
        models.Login.username == current_user.username
    ).first()
    
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    likes = db.query(models.Like).filter(
        models.Like.user_id == user_record.id
    ).all()
    
    results = []
    for like in likes:
        book = like.book
        vote_count = db.query(models.Like).filter(
            models.Like.book_id == book.id
        ).count()
        
        authors_list = book.authors.split(", ") if book.authors else []
        
        results.append({
            "google_book_id": book.google_book_id,
            "title": book.title,
            "authors": authors_list,
            "thumbnail": book.thumbnail,
            "is_liked": True,
            "vote_count": vote_count,
        })
    
    return results