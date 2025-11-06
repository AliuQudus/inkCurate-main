'''
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from . import Schemas
from fastapi.security import OAuth2PasswordBearer
from .config import Settings

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

Secret_key = Settings.SECRET_KEY

ALgorithm = Settings.ALGORITHM

Token_Expiration = Settings.TOKEN_EXPIRATION


def AccessToken(data: dict):
    encode = data.copy()

    expiration = datetime.now(timezone.utc) + timedelta(minutes=Token_Expiration)

    encode.update({"exp": int(expiration.timestamp())})

    encoded_jwt = jwt.encode(encode, Secret_key, algorithm=ALgorithm)

    return encoded_jwt


def VerifyToken(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, Secret_key, algorithms=ALgorithm)

        username: str = payload.get("username")

        if username == None:
            raise credentials_exception
        token_data = Schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return token_data


def getCurrentUser(token:str = Depends(oauth2)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW.Authenticate":"Bearer"}
    )

    return VerifyToken(token, credentials_exceptions)
    '''

from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from .import Schemas
from fastapi.security import OAuth2PasswordBearer
from .config import Settings
from uuid import UUID

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

Secret_key = Settings.SECRET_KEY
ALgorithm = Settings.ALGORITHM
Token_Expiration = Settings.TOKEN_EXPIRATION


def create_access_token(data: dict) -> str:
    """Create JWT access token - renamed from AccessToken for consistency"""
    encode = data.copy()

    # Convert UUID to string if present
    if "user_id" in encode and isinstance(encode["user_id"], UUID):
        encode["user_id"] = str(encode["user_id"])
    
    expiration = datetime.now(timezone.utc) + timedelta(minutes=Token_Expiration)
    encode.update({"exp": int(expiration.timestamp())})
    
    encoded_jwt = jwt.encode(encode, Secret_key, algorithm=ALgorithm)
    
    return encoded_jwt


# Keep the old name for backward compatibility
def AccessToken(data: dict) -> str:
    """Legacy function name - calls create_access_token"""
    return create_access_token(data)


def VerifyToken(token: str, credentials_exception):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, Secret_key, algorithms=[ALgorithm])
        
        username: str = payload.get("username")
        email: str = payload.get("email")  # Added email support
        userid: str= payload.get("user_id")
        
        if username is None:
            raise credentials_exception
        
        user_id = UUID(userid) if userid else None
        token_data = Schemas.TokenData(username=username, email=email, id=user_id)
        
    except JWTError:
        raise credentials_exception
    
    return token_data


def getCurrentUser(token: str = Depends(oauth2)) -> Schemas.TokenData:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    return VerifyToken(token, credentials_exception)


# def get_optional_current_user(token: Optional[str] = Depends(oauth2)) -> Optional[Schemas.TokenData]:
#     """
#     Get current user if authenticated, None otherwise.
#     Doesn't raise error if no token provided - useful for optional auth.
#     """
#     if token is None:
#         return None
    
#     try:
#         payload = jwt.decode(token, Secret_key, algorithms=[ALgorithm])
#         username: str = payload.get("username")
#         email: str = payload.get("email")
        
#         if username is None:
#             return None
            
#         return Schemas.TokenData(username=username, email=email)
        
#     except JWTError:
#         return None