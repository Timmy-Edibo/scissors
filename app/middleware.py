
from datetime import timezone
from datetime import datetime, timedelta

from app.models import models
from app.schemas import users
from  app.database.db import get_db

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# from jose import JWTError, jwt
from sqlalchemy.orm import Session
from jose import JWTError, jwt


import os
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = SECRET_KEY = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme= OAuth2PasswordBearer(tokenUrl='/api/v1/users/login')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None: 
            raise credentials_exception
        token_data = users.TokenData(id=id)
    except JWTError as e:
        raise credentials_exception from e

    return token_data


# Getting user token
def get_token_user(token: str = Depends(oauth2_scheme)):
    return token


# For getting current user
def get_current_user(access_token: str = Depends(oauth2_scheme), 
                    db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"})


    # Check if blacklisted token
    # if blacklist_token := auth_cruds.find_blacklist_token(db, access_token):
    #     raise credentials_exception

    token = verify_access_token(access_token, credentials_exception)
    return db.query(models.User).filter(models.User.id == token.id).first()