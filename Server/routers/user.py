from fastapi import Body, Depends, APIRouter, HTTPException, status, Path
from .. import Schemas, models, utils, Oauth
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
    
    newReg = models.Login(**user.model_dump())

    db.add(newReg)
    db.commit()
    db.refresh(newReg)

    return newReg
    

@router.delete("/{username}", status_code=status.HTTP_200_OK)
def deleteUser(username: str = Path(..., pattern="^[A-Za-z0-9_ ]+$")
, db:Session = Depends(get_db), current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser)):

    existing_user = db.query(models.Login).filter(models.Login.username ==username).first()

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No record found for the user '{username}'"
        )
    
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only delete your own account"
        )
    
    db.query(models.Login).filter(models.Login.username==username).delete(synchronize_session=False)

    # existing_user.delete(synchronize_session=False)
    db.commit()

    return  {
        "message": f"Account '{username}' have been successfully deleted"
    }
    


@router.put("/{username}", response_model=Schemas.UpdateOutput)
def updateUser(
    username: str = Path(..., pattern="^[A-Za-z0-9_ ]+$"),
    user: Schemas.UpdateUser = Body(...),
    db: Session = Depends(get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):
    if not current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data",
        )

    UserExist = db.query(models.Login).filter(models.Login.username == username).first()

    if UserExist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found",
        )

    if UserExist.username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to update this user",
        )

    InfoUpdate = user.model_dump(exclude_unset=True)
    

    if "username" in InfoUpdate and InfoUpdate["username"] != username:
        ExistingUsername = db.query(models.Login).filter(
            models.Login.username == InfoUpdate["username"]
        ).first()
        
        if ExistingUsername:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{InfoUpdate['username']}' already exists"
            )
    
    if "password" in InfoUpdate:
        InfoUpdate["password"] = utils.pwd_context.hash(InfoUpdate["password"])

    user_query = db.query(models.Login).filter(
        models.Login.username == username
    )

    user_query.update(InfoUpdate, synchronize_session=False)
    db.commit()

    
    UpdatedUsername = InfoUpdate.get("username", username)
    updated_user = db.query(models.Login).filter(models.Login.username == UpdatedUsername).first()

    return updated_user