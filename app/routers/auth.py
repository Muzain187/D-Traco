from fastapi import APIRouter, Depends, HTTPException, Request, status,Response
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, RegistrationUserRepsonse,UserLogin, PasswordResetRequest, ChangePassword
from app.dependencies.database_utils import get_db, get_password_hashed, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import config
from app.services.send_email import send_transactional_email

router = APIRouter()

#   REGISTER
@router.post('/register/', status_code=status.HTTP_201_CREATED, response_model=RegistrationUserRepsonse)
async def register(request: Request, user_credentials: UserCreate, db: Session = Depends(get_db)):
    email_check = db.query(User).filter(User.email ==user_credentials.email).first()
    if email_check != None:
       raise HTTPException(
        detail='Email is already registered',
        status_code= status.HTTP_409_CONFLICT
       )
      # hash the password
    hashed_password =  get_password_hashed(user_credentials.password)
    user_credentials.password = hashed_password
    new_user = User( email=user_credentials.email,
    username=user_credentials.username,
    password=user_credentials.password)


    token = config.token(user_credentials.email)

    email_verification_endpoint = f'http://127.0.0.1:3000/confirm-email/{token}/'
    mail_body = {
    'email':user_credentials.email,
    'project_name': "Data Investigo",
    'url': email_verification_endpoint
    }
    to = [{
        "email":str(user_credentials.email),
        'name':str(user_credentials.username)
    }]
    mail_status =await send_transactional_email(subject="Email Verification: Registration Confirmation",
    to=to, body=dict(mail_body))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
            "status_code":status.HTTP_201_CREATED,
             "message": "User registration successful",
             "data": new_user
           }


#   LOGIN
@router.post('/login/', status_code=status.HTTP_200_OK)
async def login(request: Request, user_credentials:UserLogin, db: Session = Depends(get_db)):
    # Filter search for user
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account Not Verified"
        )

    access_token = config.create_access_token(data={'user_id': user.id})
    return {
        'status_code':status.HTTP_200_OK,
        'access_token': access_token,
        'token_type': 'bearer',
        'username':user.username,
        'is_verified':user.is_verified,
        'email':user.email,
        'user_id':user.id,
    }

@router.post('/forgot-password/', status_code=status.HTTP_200_OK)
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )

    # Save the reset token to the user in the database (you need to have a field in your User model for this)
    db.commit()

    reset_token = config.token(user.email)
    # Send email with the reset link
    reset_password_endpoint = f'http://localhost:3000/resetPassword/{reset_token}'
    mail_body = {
        'email': user.email,
        'project_name': "BotBlogR",
        'url': reset_password_endpoint
    }
    mail_status = await send_transactional_email(subject="Password Reset",
                                         email_to=user.email, body=dict(mail_body))

    return {
        'status_code': status.HTTP_200_OK,
        'message': 'Password reset email sent successfully',
        'email': user.email
    }


@router.post('/reset-password/', status_code=status.HTTP_200_OK)
async def reset_password(token: str, change_password_data: ChangePassword, db: Session = Depends(get_db)):
    token_data = config.verify_token(token)
    print(token_data)
    if not token_data:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail= "Token for Email Verification has expired."
        )
    
    user = db.query(User).filter(User.email==token_data['email']).first()
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired token"
        )

    # Verify the token (you need to implement verify_token)
    if not config.verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Hash the new password
    new_hashed_password = get_password_hashed(change_password_data.new_password)

    # Update the user's password in the database and clear the reset token
    user.password = new_hashed_password
    user.reset_password_token = None
    db.commit()

    return {"message": "Password reset successful"}

@router.post('/confirm-email/{token}/', status_code=status.HTTP_202_ACCEPTED)
async def user_verification(token:str, db:Session=Depends(get_db)):
    token_data = config.verify_token(token)
    if not token_data:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail= "Token for Email Verification has expired."
        )
    user = db.query(User).filter(User.email==token_data['email']).first()

    if not user:
        raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= f"User with email {user.email} does not exist"
        )
    user.is_verified = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
    'message':'Email Verification Successful',
    'status':status.HTTP_202_ACCEPTED
    }