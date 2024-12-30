from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import User
from .schemas import UserCreate, UserResponse
from passlib.context import CryptContext
from typing import List


app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app connected to Neon PostgreSQL"}

# Create a user
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        profile_image_url=user.profile_image_url,
        is_active=user.is_active,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get all users
@app.get("/users/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Get user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user by ID
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.password_hash = pwd_context.hash(user.password)
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.profile_image_url = user.profile_image_url
    db_user.is_active = user.is_active
    db_user.is_admin = user.is_admin
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete user by ID
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted"}
