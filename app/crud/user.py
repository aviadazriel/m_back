from sqlalchemy.orm import Session

from app.configs import  hash_password
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import  HTTPException


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(user_id: int, user: UserCreate, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db_user.password = hash_password(user.password)
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.profile_image_url = user.profile_image_url
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user(db: Session, user: UserCreate):

    db_user = User(
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        profile_image_url=user.profile_image_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
