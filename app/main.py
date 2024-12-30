# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from .database import engine, Base, get_db
# from .models import User
# from .schemas import UserCreate, UserResponse

# from typing import List


# Password hashing
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")








from fastapi import FastAPI
from app.routes import user, article
from app.database import Base, engine

# Initialize app and database
app = FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app connected to Neon PostgreSQL"}

# Include routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(article.router, prefix="/articles", tags=["articles"])
