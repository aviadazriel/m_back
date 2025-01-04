# Create a user
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate
from ..models.user import Token
from ..utils.auth import generate_verification_code, send_verification_code, hash_password, verify_password

router = APIRouter()

from app.auth import get_current_user, create_access_token


@router.get("/me")
def get_user_details(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch user details from the database
    user = db.execute("SELECT id, email, first_name, last_name, phone FROM users WHERE email = :email", {"email": current_user["sub"]}).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
    }



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


