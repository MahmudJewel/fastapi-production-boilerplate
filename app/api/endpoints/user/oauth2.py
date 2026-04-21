# fastapi 
from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta

# sqlalchemy
from sqlalchemy.orm import Session

# auth google 
from starlette.requests import Request
from starlette.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth

# import 
from app.core.dependencies import get_db
from app.models import user_model as UserModel
from app.api.endpoints.user import user_function as user_functions
from app.schemas.user_schema import Token
from app.utils.env import (
    ACCESS_TOKEN_EXPIRE_DAYS, 
    REFRESH_TOKEN_EXPIRE_DAYS, 
    GOOGLE_CLIENT_ID, 
    GOOGLE_CLIENT_SECRET, 
    REDIRECT_URI
    ) 
social_auth_module = APIRouter()

# google ========================
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=REDIRECT_URI,
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs', # added
)

# ============================> signin using google <========================
@social_auth_module.get('/google/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    print(f"Redirect URI=========================>: {redirect_uri}")
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    return response

@social_auth_module.get('/auth/google/callback') # path will be same as redirect url
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    # google = oauth.create_client('google')
    # token = await google.authorize_access_token(request)
    if 'id_token' not in token:
        raise HTTPException(status_code=400, detail="Missing id_token in response")
    # user = await oauth.google.parse_id_token(request, token)
    # user_info = await oauth.google.parse_id_token(request, token)
    # ===> no need to parse_id_token. starlet will do parse_id_token automatically. 
    user_info = token['userinfo']
    # Extract user information
    email = user_info['email']
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')
    is_verified = user_info.get('email_verified', False)
    print(f"user info ===================> {user_info}")
    # Check if user already exists
    user = await user_functions.get_user_by_email(db=db, email=email)
    # user = db.query(UserModel.User).filter(UserModel.User.email == email).first()
    if user is None:
        # Create a new user
        user = UserModel.User(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update existing user
        user.first_name = first_name
        user.last_name = last_name
        db.commit()

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = user_functions.create_access_token(
        data={"id": user.id, "email": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = await user_functions.create_refresh_token(
        data={"id": user.id, "email": user.email, "role": user.role}, 
        expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    # return JSONResponse({
    #     'email': user.email,
    #     'first_name': user.first_name,
    #     'last_name': user.last_name,
    #     'is_verified': is_verified
    # })

# @auth_module.get('/protected')
# async def protected(user: dict = Depends(oauth.google.authorize_user)):
#     return {'message': 'This is a protected route', 'user': user}