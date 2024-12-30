from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://<username>:<password>@<host>/<database>"
DATABASE_URL = "postgresql://mashkanta_portal_owner:DG5OfFcImwT3@ep-winter-river-a5z1n6xh.us-east-2.aws.neon.tech/mashkanta_portal?sslmode=require"
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
