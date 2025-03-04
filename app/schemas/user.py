#app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
   username: str
   email: EmailStr
   password:str
   is_verified: bool=False

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
   
    class Config:
       from_attributes = True
       
class RegistrationUserRepsonse(BaseModel):
    message:str
    data: UserResponse

class ChangePassword(BaseModel):
    new_password:str
    confirm_password:str


class PasswordResetRequest(BaseModel):
    email: EmailStr
