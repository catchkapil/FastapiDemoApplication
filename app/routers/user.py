from typing import List, Optional
from .. import schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from .. import models
from .. import utils
from ..database import get_db

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreatedResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserCreatedResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"user with id : {id} not found")
    return user
