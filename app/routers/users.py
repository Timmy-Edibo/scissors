from fastapi import (APIRouter, 
                     Depends,UploadFile, 
                     BackgroundTasks)

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.users import User, Token

from app.database.db import get_db
from sqlalchemy.orm import Session
from app.middleware import get_current_user


from app.cruds import users

user_router = APIRouter(prefix="/api/v1/users", tags=['users'])

@user_router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
            db: Session = Depends(get_db)):
    return users.login(user_credentials, db)

@user_router.get("/get")
def get_user(email: EmailStr, db:Session=Depends(get_db),
             current_user:Session=Depends(get_current_user)):
    
   return users.get_user(email, db)
    
@user_router.get("/list-all")
def list_user(db:Session=  Depends(get_db), current_user:Session=Depends(get_current_user)):
    return users.list_user(db)

@user_router.post("/register")
async def  register_user(request: User, background_tasks: BackgroundTasks, 
                         db: Session = Depends(get_db)):
    return users.register_user(request, background_tasks, db)
    

@user_router.get("/activate-user")
async def user_confirmation_otp(otp: str, db: Session = Depends(get_db)):
    return users.activate_user(otp, db)



@user_router.post("/block")
def block_user(email: EmailStr, db:Session=Depends(get_db), 
               current_user:Session=Depends(get_current_user)):
    
    return users.block_user(email, db)

@user_router.post("/unblock")
def unblock_user(email: EmailStr, db:Session=Depends(get_db),
                 current_user:Session=Depends(get_current_user)):
    
    return users.unblock_user(email, db)

@user_router.post("/send-reset-password-link")
async def  send_reset_password_link(email: EmailStr,
                    background_tasks:BackgroundTasks, 
                    db: Session = Depends(get_db)):
    
    return users.send_reset_password_link(email, background_tasks, db)
 
@user_router.put("/update-profile-photo")
async def upload_profile_photo(id: int, image:UploadFile, 
                    db: Session = Depends(get_db), 
                    current_user:Session=Depends(get_current_user)):
    
    return users.upload_profile_photo(id, image, db) 


@user_router.put("/reset-password")
def reset_user_password(token: str, new_password: str, 
                        db: Session = Depends(get_db)):
    
    return users.reset_user_password(token, new_password, db)
    

@user_router.put("/update")
def update_user(request: User, db:Session=Depends(get_db),
                current_user:Session=Depends(get_current_user)):
    
    return users.update_user(request, db)


@user_router.delete("/delete")
def delete_user(email: EmailStr, db:Session=Depends(get_db),
                current_user:Session=Depends(get_current_user)):
    
    return users.delete_user(email, db)
    
@user_router.delete("/delete-all-user")
def delete_all_user(db:Session=  Depends(get_db),
                    current_user:Session=Depends(get_current_user)):
    
    return users.delete_all_user(db)

@user_router.get("/me")
def current_loggedin_user(db:Session=  Depends(get_db),
                    current_user:Session=Depends(get_current_user)):
    
    return current_user
