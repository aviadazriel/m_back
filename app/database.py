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

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
