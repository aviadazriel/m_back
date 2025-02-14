from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
# Database Configuration
DB_HOST = os.getenv("RDS_HOST")
DB_PORT = os.getenv("RDS_PORT")
DB_USER = os.getenv("RDS_USER")
DB_PASSWORD = os.getenv("RDS_PASSWORD")
DB_NAME = os.getenv("RDS_DATABASE")


# DATABASE_URL = "postgresql://<username>:<password>@<host>/<database>"
# DATABASE_URL = "postgresql://mashkanta_portal_owner:DG5OfFcImwT3@ep-winter-river-a5z1n6xh.us-east-2.aws.neon.tech/mashkanta_portal?sslmode=require"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from datetime import datetime, timedelta


# -- הגדרות בסיסיות ל-DB (PostgreSQL)
metadata = MetaData(bind=engine)

# -- הגדרת הטבלאות ב-SQLAlchemy (אפשר גם ב-ORM מלא, כאן דוגמה בטאבלת Metadata)
users_table = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("phone", String, unique=True, nullable=False),
    Column("password", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("is_verified", Boolean, default=False),
)

sessions_table = Table(
    "sessions", metadata,
    Column("session_id", PG_UUID(as_uuid=True), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
    Column("expires_at", DateTime),
    Column("data", JSONB),
)


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
