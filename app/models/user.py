from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from app.database import Base
from sqlalchemy import Column, Integer, String, Text, Date, ARRAY, TIMESTAMP

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(10), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    profile_image_url = Column(String)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))

