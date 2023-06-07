from pydantic import BaseModel, EmailStr
from typing import Optional



class ShortenUrl(BaseModel):
    long_url: str
    custom_url: Optional[str] = None
