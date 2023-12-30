from datetime import datetime, timedelta
from jwt import encode as jwt_encode , decode as jwt_decode, PyJWTError
import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature,SignatureExpired
from pydantic import EmailStr
from app.models.user import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.dependencies.database_utils import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



token_algo= URLSafeTimedSerializer(SECRET_KEY,salt='Email_Verification_&_Forgot_password')

def token(email: EmailStr):
    _token = token_algo.dumps(email)
    return _token

def verify_token(token:str):
    try:
      email = token_algo.loads(token, max_age=1800)
    except SignatureExpired:
       return None
    except BadTimeSignature:
     return None
    return {'email':email, 'check':True}


async def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        user=db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user 
    except PyJWTError:
        raise credentials_exception