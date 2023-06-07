import random
from app.database.db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models import models


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def generate_reset_password_otp() -> str:
    return str(random.randint(100000, 999999))

def create_reset_password_token(email: str, phone_number:str, db: Session = Depends(get_db)):
    token =generate_reset_password_otp()
    query= models.ResetPasswordToken(email=email, phone_number=phone_number, code=token)
    db.add(query)
    db.commit()
    db.refresh(query)
    
    reset_password_link_mailer(email, token)

def reset_password_link_mailer(email, token):
    # Email login credentials
    email_sender = 'timothyedibo@gmail.com'
    email_password = 'mnrgigkqkkuvdzxd'

    # Create message object instance
    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email
    message['Subject'] = 'Chatter Reset Password Link'
    reset_link = f"http://127.0.0.1:8000/api/v1/users/reset-password?otp={token}" 

    # Add message body
    body = f'<p>Here is your reset password link: <a href="{reset_link}">Click here</a>. It expires in 10 minutes. Neglect if this email is not triggered by you.</p>'
    message.attach(MIMEText(body, "html"))
    
    
    # Create SMTP session
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    session = smtplib.SMTP_SSL(smtp_server, smtp_port)

    # Login to email account
    session.login(email_sender, email_password)

    try:
        session.sendmail(email_sender, email, message.as_string())
        print(f'Successfully sent email to {email} with OTP {token}')
    except smtplib.SMTPException as e:
        print(f'Error: {str(e)}')

    # Close the session
