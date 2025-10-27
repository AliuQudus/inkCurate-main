from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. import Schemas, models, utils, Oauth
from ..database import get_db

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_details: Schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.Login).filter(
        models.Login.email == user_details.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )
    
    if not utils.pwd_context.verify(user_details.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )

    access_token = Oauth.create_access_token(
        data={"username": user.username, "email": user.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser)):
    return {
        "message": f"User {current_user.username} successfully logged out. Please remove the token from client storage."
    }