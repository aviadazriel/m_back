import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
# Database Configuration
SECRET_KEY = os.getenv("SECRET_KEY")

# Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)