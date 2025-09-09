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