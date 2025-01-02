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
from app.routes import user, article, news, chat
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Initialize app and database
app = FastAPI()
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],  # Allow specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app connected to Neon PostgreSQL"}


@app.get("/gitchanges")
def read_root():
    return {"message": "gitchanges"}

# Include routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(article.router, prefix="/articles", tags=["articles"])
app.include_router(news.router, prefix="/news", tags=["news"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

# python -m uvicorn app.main:app --reload


