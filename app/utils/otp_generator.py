import random
from app.database.db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models import models


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def create_otp(email: str, phone_number:str, db: Session = Depends(get_db)):
    code = generate_otp()
    query= models.Otp(email=email, phone_number=phone_number, code=code)
    db.add(query)
    db.commit()
    db.refresh(query)

    mailer(email, code)

def mailer(email, otp):
    # Email login credentials
    email_sender = 'timothyedibo@gmail.com'
    email_password = 'mnrgigkqkkuvdzxd'

    # Create message object instance
    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email
    message['Subject'] = 'Scissors User Confirmation'
    link = f'http://127.0.0.1:8000/api/v1/users/activate-user?otp={otp}'
    

    # Add message body
    message.attach(MIMEText(f'Welcome to Scissors. Click on the link to activate account. {link} It expires in 10mins'))

    # Create SMTP session
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    session = smtplib.SMTP_SSL(smtp_server, smtp_port)

    # Login to email account
    session.login(email_sender, email_password)

    try:
        session.sendmail(email_sender, email, message.as_string())
        print(f'Successfully sent email to {email} with OTP {otp}')
    except smtplib.SMTPException as e:
        print(f'Error: {str(e)}')

    # Close the session
