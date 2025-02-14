from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional

from app.configs import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.database import sessions_table, get_db, users_table
import uuid
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, Request, Response, HTTPException, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import select, insert, delete
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# # Get current user
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return {"sub": email}  # Return user email from token
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")





def get_current_user(request: Request, db=Depends(get_db)):
    # שליפת ה-cookie
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not logged in (no session)")

    # בדיקת הסשן ב-DB
    sess = db.execute(select(sessions_table).where(sessions_table.c.session_id == session_id)).fetchone()
    if not sess:
        raise HTTPException(status_code=401, detail="Session not found")

    # בדיקת תאריך תפוגה
    if sess.expires_at and sess.expires_at < datetime.utcnow():
        # סשן פג תוקף => מוחקים מה-DB
        db.execute(delete(sessions_table).where(sessions_table.c.session_id == session_id))
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired")

    # שליפת המשתמש
    user = db.execute(select(users_table).where(users_table.c.id == sess.user_id)).fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
