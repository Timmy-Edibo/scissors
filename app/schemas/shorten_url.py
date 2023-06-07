from pydantic import BaseModel, EmailStr
from typing import Optional



class ShortenUrl(BaseModel):
    long_url: str
    custom_url: Optional[str] = None
    
    class Meta:
        orm_mode=True



class UpdateShortenUrl(ShortenUrl):
    short_url: str
    long_url: str
    custom_url: Optional[str] = None
    
    
    