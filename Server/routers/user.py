
from fastapi import Depends, APIRouter, HTTPException, status
from .. import Schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/Reg", tags=["Registration"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[Schemas.UserResponse],
)
def users(db: Session = Depends(get_db)):
    user = db.query(models.Login).all()
    return user

@router.post("", status_code=status.HTTP_200_OK, response_model=Schemas.UserResponse)
def CreateUser(user:Schemas.User, db: Session = Depends(get_db)):
    
    EmailExist = (db.query(models.Login).filter(models.Login.email==user.email).first())

    if EmailExist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with '{user.email}' already exist"
        )
    

    UserExist = (db.query(models.Login).filter(models.Login.username==user.username).first())

    if UserExist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{user.username}' already exist"
        )
    
    user.password = (utils.pwd_context.hash(user.password))
  

    # hashed_password = utils.pwd_context.hash(user.password)
    # user.password = hashed_password

    
    newReg = models.Login(**user.model_dump())

    db.add(newReg)
    db.commit()
    db.refresh(newReg)

    return newReg
    