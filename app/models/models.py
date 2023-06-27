from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database.db import Base
from datetime import datetime, timedelta, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_number =Column(String(20))
    address = Column(String(50))
    profile_photo = Column(String)
    is_active = Column(Boolean, default=True)
    time_created = Column(DateTime, server_default=func.now())
    
    short_url = relationship("ShortenUrl", back_populates = "user_table")
    otp_table = relationship("Otp", back_populates = "user_otp_table")
    reset_password_token = relationship("ResetPasswordToken", back_populates = "reset_password_token_table")




class Otp(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6))
    email = Column(ForeignKey(User.email, ondelete="CASCADE"), nullable=False)
    phone_number =Column(String(20))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    expire_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user_otp_table = relationship("User", back_populates = "otp_table")
    
    def __init__(self, code, email, phone_number=None, expire_seconds=900):
        self.code = code
        self.email = email
        self.phone_number = phone_number
        self.time_created = datetime.now(timezone.utc)
        self.expire_at = self.time_created + timedelta(seconds=expire_seconds)
    
        print(self.time_created)
    
    


class ResetPasswordToken(Base):
    __tablename__ = "reset_password_token"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6))
    email = Column(ForeignKey(User.email, ondelete="CASCADE"), nullable=False)
    phone_number =Column(String(20))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    expire_at = Column(DateTime(timezone=True), server_default=func.now())
    
    reset_password_token_table = relationship("User", back_populates = "reset_password_token")
    
    def __init__(self, code, email, phone_number=None, expire_seconds=900):
        self.code = code
        self.email = email
        self.phone_number = phone_number
        self.time_created = datetime.now(timezone.utc)
        self.expire_at = self.time_created + timedelta(seconds=expire_seconds)
    
        print(self.time_created)
    
       
class ShortenUrl(Base):
    __tablename__ = "shorten_url"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(ForeignKey(User.email, ondelete="CASCADE"), nullable=False)
    short_url = Column(String, unique=True, nullable=False)
    custom_url = Column(String, nullable=False)
    long_url = Column(String, nullable=True)
    qrcode = Column(String, nullable=True)
    
    user_table = relationship("User", back_populates = "short_url")