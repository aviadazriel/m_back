from typing import List

# Create a user
from ..models.user import User, Token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user, update_user
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
router = APIRouter()




# Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.post("/", response_model=UserResponse)
def create_user_post(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user


# Get all users
@router.get("/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user by ID
@router.put("/{user_id}", response_model=UserResponse)
def update_user_id(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(user_id, user, db)

# Delete user by ID
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted"}



# Utility Functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

# # todo: build it better
# # Routes
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.execute("SELECT * FROM users WHERE email = :email", {"email": user.email}).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db.execute(
        "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)",
        {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "password": hashed_password},
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