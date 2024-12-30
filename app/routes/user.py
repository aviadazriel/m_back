from typing import List

# Create a user
from ..models.user import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user, update_user

router = APIRouter()

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