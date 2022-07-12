from fastapi import Depends, HTTPException, status, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas
from .. import models
from .. import utils
from .. import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['authentication'])


@router.post('/login', response_model=schemas.UserToken)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"user with email : {user_credentials.email} not found")

    if not utils.verify_hash(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"passoword entered is incorrect")

    encoded_token = oauth2.create_access_token(data={'user_id': user.id})

    return {"access_token": encoded_token, "token_type": 'bearer'}
