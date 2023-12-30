# app/dependencies/database_utils.py

from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from passlib.context import CryptContext

# Define a global instance of CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hashed(password: str) -> str:
    """
    Hash the password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
