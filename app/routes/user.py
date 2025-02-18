# Create a user
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from app.database import get_db, sessions_table
from app.schemas.user import UserCreate
from ..models.user import Token, User
from ..utils.auth import generate_verification_code, send_verification_code, hash_password, verify_password, \
    send_reset_email, set_session_id

import uuid
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, Request, Response, HTTPException, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import select, insert, delete
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt



router = APIRouter()

from app.auth import get_current_user, create_access_token


from google.oauth2 import id_token
from google.auth.transport import requests
GOOGLE_CLIENT_ID = "1040890287209-6ei904rpmlpsp7m3gs42eietl4e3pn3h.apps.googleusercontent.com"

from pydantic import BaseModel

# Request model to accept the token in the request body
class GoogleLoginRequest(BaseModel):
    token: str











class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    phone: str
    password: str
    first_name: str
    last_name: str





@router.post("/google-login")
def google_login(request: GoogleLoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        token = request.token
        # Verify the Google token
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        print(id_info)

        # Extract user information
        email = id_info.get("email")
        first_name = id_info.get("given_name")
        last_name = id_info.get("family_name", "")

        if not email:
            raise HTTPException(status_code=400, detail="Google account email not found")

        # Check if the user already exists
        user = db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchone()

        if not user:
            db.execute(
                "INSERT INTO users (first_name, last_name, email, google_id, is_google_user, is_verified) VALUES (:first_name, :last_name, :email, :google_id, :is_google_user, :is_verified)",
                {"first_name": first_name, "last_name": last_name, "email": email, "google_id": id_info.get("sub"), "is_google_user": True, "is_verified": True},
            )

            # Register the user if they don't exist
            # db.execute(
            #     "INSERT INTO users (first_name, last_name, email, is_verified) VALUES (:first_name, :last_name, :email, :is_verified)",
            #     {"first_name": first_name, "last_name": last_name, "email": email, "is_verified": True},
            # )
            db.commit()


        session_id = set_session_id(db, user.id)
        db.close()

        # 6) הגדרת ה-Cookie בתגובה
        # בדוגמה הבסיסית - httpOnly = False כדי שאפשר לראות ולבדוק; בסט-אפ ייצור תרצה True
        response.set_cookie(
            key="session_id",
            value=str(session_id),
            httponly=True,  # להגנה מפני XSS
            max_age=10800,  # 3 שעות
            # samesite="lax",  # או strict
            samesite="None",
            secure=True  # בפרודקשן רצוי True אם HTTPS
        )

        return {"message": "Logged in successfully"}

        # # Create a JWT token
        # access_token = create_access_token(data={"sub": email})
        # return {"access_token": access_token, "token_type": "bearer"}


    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")



import re

def validate_phone_number(phone):
    """
    Validates if the input phone number is exactly 10 digits.
    """
    pattern = r"^\d{10}$"  # Regex for exactly 10 digits
    if re.fullmatch(pattern, phone):
        return True, "Valid phone number."
    else:
        return False, "מספר הטלפון לא בפורמט הנכון (שימו לב לכמות הספרות וללא סימנים מיוחדים)"



# , response_model=Token
# # Routes
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.execute("SELECT * FROM users WHERE email = :email", {"email": user.email}).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="אימייל קיים במערכת")
    is_valid, message = validate_phone_number(user.phone)
    if not user.phone or not is_valid:

        raise HTTPException(status_code=400, detail=message)

    existing_user_phone = db.execute("SELECT * FROM users WHERE phone = :phone", {"phone": user.phone}).fetchone()
    if existing_user_phone:
        raise HTTPException(status_code=400, detail="מספר הטלפון כבר קיים במערכת")
    #
    # Generate a verification code
    verification_code = generate_verification_code()

    hashed_password = hash_password(user.password)
    db.execute(
        "INSERT INTO users (first_name, last_name, email, password, phone, is_verified, verification_code) VALUES (:first_name, :last_name, :email, :password, :phone, :is_verified, :verification_code)",
        {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "password": hashed_password,
         "phone": user.phone,
         "is_verified": False,
         "verification_code": verification_code},
    )
    db.commit()
    db.close()

    send_verification_code(user.email, f"{user.first_name} {user.last_name}", verification_code)
    return {"info": "send_verification_code"}
    # access_token = create_access_token(data={"sub": user.email})
    # return {"access_token": access_token, "token_type": "bearer"}


class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login") #, response_model=Token
def login(request: LoginRequest, response: Response,  db: Session = Depends(get_db)):
    print(request.email)
    user = db.execute("SELECT * FROM users WHERE email = :email", {"email": request.email}).fetchone()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Phone number not verified")
    # access_token = create_access_token(data={"sub": user.email})

    session_id = set_session_id(db, user.id)
    db.close()

    # 6) הגדרת ה-Cookie בתגובה
    # בדוגמה הבסיסית - httpOnly = False כדי שאפשר לראות ולבדוק; בסט-אפ ייצור תרצה True
    response.set_cookie(
        key="session_id",
        value=str(session_id),
        httponly=True,  # להגנה מפני XSS
        max_age=10800,  # 3 שעות
        samesite="None",  # או strict  #todo:lax   none
        secure=True  # בפרודקשן רצוי True אם HTTPS #todo
    )


    return {"message": "Logged in successfully"}


    # return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-phone")
def verify_phone(phone: str, code: int, db: Session = Depends(get_db)):
    print(phone)
    user = db.execute("SELECT * FROM users WHERE phone = :phone", {"phone": phone}).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    # Mark the user as verified
    db.execute("UPDATE users SET is_verified = True WHERE phone = :phone", {"phone": phone})
    db.commit()

    return {"message": "Phone number verified successfully"}

import secrets
from pydantic import BaseModel

class EmailRequest(BaseModel):
    email: str

reset_tokens = {}
@router.post("/reset-password")
def reset_password(request: EmailRequest, db: Session = Depends(get_db)):
    email = request.email
    user = db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

        # Generate a secure token
    token = secrets.token_urlsafe(32)
    reset_tokens[token] = user.email

    # Send password reset email
    # Send the reset link via email
    reset_link = f"http://localhost:3000/reset-password/{token}"
    send_reset_email(email, reset_link)
    return {"message": "Password reset link sent to your email"}

class NewPasswordRequest(BaseModel):
    new_password: str
    token: str
# Reset the password using the token
@router.post("/reset-new-password")
def reset_password(request: NewPasswordRequest, db: Session = Depends(get_db)):
    email = reset_tokens.get(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Find the user by email and update the password
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(request.new_password)
    db.commit()

    # Remove the token from the store
    del reset_tokens[request.token]

    return {"message": "Password reset successful"}


import shutil
from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException
@router.get("/me")
def get_user_details(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "phone": current_user.phone,
        # "address": user.address,
        # "status": user.status,
        # "profile_image": current_user.profile_image_url,
    }

from typing import Optional

@router.put("/update")
async def update_user(
    firstName: str = Form(...),
    lastName: str = Form(...),
        phone: Optional[str] = Form(None),
        address: Optional[str] = Form(None),
        status: Optional[str] = Form(None),
        profileImage: Optional[UploadFile] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.first_name = firstName
    user.last_name = lastName
    user.phone = phone
    # user.address = address
    # user.status = status

    if profileImage:
        image_path = f"uploads/{profileImage.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(profileImage.file, buffer)
        user.profile_image_url = image_path

    db.commit()
    return {"message": "Profile updated successfully"}





# -----------------------------------------------------
# נתיב שמחייב משתמש מחובר
# -----------------------------------------------------
@router.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {
        "message": "You are in a protected route",
        "user_id": current_user.id,
        "email": current_user.email,
    }

# -----------------------------------------------------
# LOGOUT
# -----------------------------------------------------
@router.post("/logout")
def logout(request: Request, response: Response, db=Depends(get_db)):
    session_id = request.cookies.get("session_id")
    if session_id:
        db.execute(delete(sessions_table).where(sessions_table.c.session_id == session_id))
        db.commit()

        # מוחקים/מרוקנים את העוגייה
        response.delete_cookie("session_id")

    return {"message": "Logged out successfully"}