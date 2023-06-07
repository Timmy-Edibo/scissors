from fastapi import ( Depends, HTTPException, 
                     status, UploadFile, 
                     BackgroundTasks)

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.utils.password_util import hash, verify
from pydantic import EmailStr

from app.schemas.users import User, Otp
from app.models import models
from app.database.db import get_db
from sqlalchemy.orm import Session

from app.utils.otp_generator import create_otp
from app.utils.reset_password import create_reset_password_token

from app.middleware import create_access_token, get_current_user



def  register_user(request: User, background_tasks: BackgroundTasks, 
                         db: Session = Depends(get_db)):
    
    user_request = models.User(**request.dict())
    user_request.hashed_password = hash(request.hashed_password)
    
    if db.query(models.User).filter(
        models.User.email == user_request.email).first():
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="email is already in use")
        
    db.add(user_request)
    db.commit()
    db.refresh(user_request)
    
    background_tasks.add_task(create_otp, request.email, request.phone_number, db)
     
    return {"data": user_request, "status": status.HTTP_201_CREATED}


def activate_user(otp: str, db: Session = Depends(get_db)):
    
    query = db.query(models.Otp).filter(models.Otp.code == otp).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="otp is not found")
                
    user = db.query(models.User).filter(models.User.email == query.email)
    user.update({'is_active': True})
    db.commit()
    
    return {"data": 'Welcome to chatters, your account successfully activated', "status": status.HTTP_201_CREATED}


def upload_profile_photo(id: int, image:UploadFile,  db: Session = Depends(get_db)):
    
    query =  db.query(models.User).filter(
        models.User.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")
                
    #pushimage to clodinary and store url in db
    
    query.update({"profile_photo": image.filename}, synchronize_session=False)
    db.commit()

    return {"data": query.first(), "status": status.HTTP_201_CREATED}


async def  send_reset_password_link(email: EmailStr,
    background_tasks:BackgroundTasks, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(
        models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="no account with email address you provided")

    background_tasks.add_task(create_reset_password_token, 
                    user.email, user.phone_number, db)
    
    return {"data": "reset password link sent successfully", 
            "status": status.HTTP_201_CREATED}


def reset_user_password(token: str, new_password: str, db: Session = Depends(get_db)):
    
    query =  db.query(models.ResetPasswordToken).filter(
        models.ResetPasswordToken.code == token)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Invalid OTP")
                    
    user =  db.query(models.User).filter(models.User.email == query.first().email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Not authorized to perform this operation")
        
    password = hash(new_password)
    user.update({'hashed_password': password})
    db.commit()
    
    return {"data": 'password has been reset successfully', "status": status.HTTP_201_CREATED}


def get_user(email: EmailStr, db:Session=Depends(get_db)):
    
    if query :=  db.query(models.User).filter(
        models.User.email == email).first():
        return {"data": query, "status": status.HTTP_201_CREATED}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")

def list_user(db:Session=  Depends(get_db)):
    query =  db.query(models.User).all()
    response = query if len(query) > 0 else "No record found in db"
    return {"data": response, "status": status.HTTP_200_OK}


def update_user(request: User, db:Session=Depends(get_db)):
    query =  db.query(models.User).filter(models.User.email == request.email)
    
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")
    query.update(**request.dict())
    db.commit()
        
    return {"data": query, "status": status.HTTP_200_OK}
        

def delete_user(email: EmailStr, db:Session=Depends(get_db)):
    
    if query :=  db.query(models.User).filter(
        models.User.email == email).first():
        db.delete(query)
        db.commit()
        
        return {"data": "User deleted successfully", "status": status.HTTP_200_OK}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")

def delete_all_user(db:Session=  Depends(get_db)):
    query =  db.query(models.User).all()
    
    for user in query:
        user = db.query(models.User).filter(models.User.id == user.id).first()
        otp = db.query(models.Otp).filter(models.Otp.email == user.email).first()
        db.delete(otp)
        db.delete(user)
        db.commit()
    
    return {"data": "Users deleted successfully", "status": status.HTTP_200_OK}


def block_user(email: EmailStr, db:Session=Depends(get_db)):
    
    if query :=  db.query(models.User).filter(
        models.User.email == email):
  
        query.update({'is_active': False})
        return {"data": "User blocked successfully", "status": status.HTTP_200_OK}


    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")


def unblock_user(email: EmailStr, db:Session=Depends(get_db)):
    
    if query :=  db.query(models.User).filter(
        models.User.email == email):
  
        query.update({'is_active': True})
        return {"data": "User blocked successfully", "status": status.HTTP_200_OK}
        

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")



def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
            db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    if user.is_active == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="This account is not active")

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")


    if not verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")


    # create a token
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}  

