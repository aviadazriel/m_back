import os
from dotenv import load_dotenv
load_dotenv()
# Database Configuration
SECRET_KEY = os.getenv("SECRET_KEY")

# Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
