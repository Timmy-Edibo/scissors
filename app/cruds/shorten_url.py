from fastapi import (APIRouter, 
                     Depends,UploadFile, 
                     BackgroundTasks)

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.shorten_url import ShortenUrl

from app.database.db import get_db
from sqlalchemy.orm import Session
from app.middleware import get_current_user



def create_shorten_url(request: ShortenUrl, db: Session = Depends(get_db),
                    current_user: Session = Depends(get_current_user)):
    pass
    
    # return {"data": user_request, "status": status.HTTP_201_CREATED}



def get_category(id: int, db: Session = Depends(get_db),
                    current_user: Session = Depends(get_current_user)):
    pass
    # return {"data": user_request, "status": status.HTTP_201_CREATED}



def list_category(db: Session = Depends(get_db),
                    current_user: Session = Depends(get_current_user)):
    pass
    # return {"data": user_request, "status": status.HTTP_201_CREATED}



def search_category(category_name: str, db: Session = Depends(get_db),
                    current_user: Session = Depends(get_current_user)):
    
    pass
    # return {"data": user_request, "status": status.HTTP_201_CREATED}




def update_category(id:int, db: Session = Depends(get_db),
                    current_user: Session = Depends(get_current_user)):
    pass
    # return {"data": user_request, "status": status.HTTP_201_CREATED}



def delete_category(id: int, db: Session = Depends(get_db),
                    current_user: Session = Depends(get_current_user)):
    pass
    # return {"data": user_request, "status": status.HTTP_201_CREATED}

