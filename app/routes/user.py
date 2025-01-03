# Create a user
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate
from ..configs import SECRET_KEY, ALGORITHM, hash_password, verify_password
from ..models.user import Token

router = APIRouter()




from app.auth import get_current_user

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

# Utility Functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



# # todo: build it better
# # Routes
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.execute("SELECT * FROM users WHERE email = :email", {"email": user.email}).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db.execute(
        "INSERT INTO users (first_name, last_name, email, password, phone) VALUES (:first_name, :last_name, :email, :password, :phone)",
        {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "password": hashed_password, "phone": user.phone},
    )
    db.commit()
    db.close()
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(form_data.__dict__)
    print(form_data.username)
    user = db.execute("SELECT * FROM users WHERE email = :email", {"email": form_data.username}).fetchone()
    print(user)
    print(user.password)
    print(user.email)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": user.email})
    db.close()
    return {"access_token": access_token, "token_type": "bearer"}


