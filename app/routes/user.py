# Create a user
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate
from ..models.user import Token, User
from ..utils.auth import generate_verification_code, send_verification_code, hash_password, verify_password, \
    send_reset_email

router = APIRouter()

from app.auth import get_current_user, create_access_token


from google.oauth2 import id_token
from google.auth.transport import requests
GOOGLE_CLIENT_ID = "1040890287209-6ei904rpmlpsp7m3gs42eietl4e3pn3h.apps.googleusercontent.com"

from pydantic import BaseModel

# Request model to accept the token in the request body
class GoogleLoginRequest(BaseModel):
    token: str
@router.post("/google-login")
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
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

        # Create a JWT token
        access_token = create_access_token(data={"sub": email})
        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")






# # todo: build it better
# # Routes
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.execute("SELECT * FROM users WHERE email = :email", {"email": user.email}).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

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

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(form_data.__dict__)
    print(form_data.username)
    user = db.execute("SELECT * FROM users WHERE email = :email", {"email": form_data.username}).fetchone()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Phone number not verified")
    access_token = create_access_token(data={"sub": user.email})
    db.close()
    return {"access_token": access_token, "token_type": "bearer"}


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
def get_user_details(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        # "address": user.address,
        # "status": user.status,
        "profile_image": user.profile_image_url,
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