from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    address: str    
    phone_number:str
    # content_table = relationship("Content", back_populates = "user_table")

class Otp(BaseModel):
    code: str
    email:EmailStr
    phone_number: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None