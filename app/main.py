# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from .database import engine, Base, get_db
# from .models import User
# from .schemas import UserCreate, UserResponse

# from typing import List


# Password hashing
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from fastapi import FastAPI, Request, Response

from app.routes import user, article, news, chat, user_manager, api_test
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Initialize app and database
app = FastAPI(redirect_slashes=False)
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3001", "http://localhost:3000"],  # Allow specific frontend URL
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000","http://localhost:3001", "http://127.0.0.1:3001",
               "https://mashkanta.netlify.app", "http://mashkanta-me.com", "https://mashkanta-me.com"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Access-Control-Allow-Origin: https://mashkanta.netlify.app
# Access-Control-Allow-Methods: POST, OPTIONS
# Access-Control-Allow-Headers: Content-Type


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app connected to Neon PostgreSQL"}

# Custom middleware to add the COOP header
@app.middleware("http")
async def add_coop_header(request: Request, call_next):
    response: Response = await call_next(request)
    # Setting COOP to allow popups to communicate via window.postMessage.
    response.headers['Cross-Origin-Opener-Policy'] = "same-origin-allow-popups"
    return response

# Include routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(user_manager.router, prefix="/users_manager", tags=["users"])
app.include_router(article.router, prefix="/articles", tags=["articles"])
app.include_router(news.router, prefix="/news", tags=["news"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(api_test.router, prefix="/api_test", tags=["test"])
# python -m uvicorn app.main:app --reload


