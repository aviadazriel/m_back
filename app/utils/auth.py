import random
from fastapi import  HTTPException

# Generate a random 6-digit verification code
from app.configs import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SERVER
from app.database import sessions_table


def generate_verification_code():
    return random.randint(100000, 999999)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_reset_email(email: str, reset_link:str):
    msg = MIMEText(f"Click the link to reset your password: {reset_link}")
    msg["Subject"] = "Password Reset"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    try:
        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500)

def send_verification_code(email, name, verification_code):
    # Set up the email message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = "קוד אימות - משכנתא מניסיון"
    # Email body with RTL styling
    body = f"""
        <html>
            <body style="direction: rtl; text-align: right; font-family: Arial, sans-serif;">
                <h2>שלום {name},</h2>
                 <p>ברוכים הבאים למשכנתא מניסיון</p>
                <p>קוד האימות שלך הוא: <strong>{verification_code}</strong></p>

            </body>
        </html>
        """
    msg.attach(MIMEText(body, "html"))

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Verification email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500)

from passlib.context import CryptContext

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

from fastapi import HTTPException

from sqlalchemy.sql import select, insert, delete

import uuid
from datetime import datetime, timedelta
def set_session_id(db, user_id):
    # 3) יצירת session_id
    session_id = uuid.uuid4()

    # 4) קביעת תפוגה (אופציונלי)
    expires_at = datetime.utcnow() + timedelta(hours=3)  # למשל סשן ל-3 שעות

    # 5) החדרת רשומה לטבלת sessions
    ins_sess = insert(sessions_table).values(
        session_id=session_id,
        user_id=user_id,
        created_at=datetime.utcnow(),
        expires_at=expires_at,
        data={}  # אפשר לשים פה הרשאות וכדומה
    )
    db.execute(ins_sess)
    db.commit()
    return session_id