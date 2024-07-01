from datetime import timedelta

import fastapi
from fastapi import Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
import requests
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse
from settings import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET,GOOGLE_REDIRECT_URL


from api.utils.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
)
from api.utils.auth import get_user as get_user_by_username

from api.utils.user import (
    create_user,
)
from common.http_exceptions import MISSMATCHAUTH
from db.db_setup import get_db
from schemas.user import UserCreate

router = fastapi.APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/auth/login", response_model=Token)
async def login(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, user.username, user.password)

    if not user:
        raise MISSMATCHAUTH
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", user: user}


@router.post("/auth/register", response_model=Token, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username is already registered")

    user = create_user(db=db, user=user)

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", user: user}

@router.get('/login/google')
def login():
    
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URL}"
        f"&scope=openid email profile"
    )
    return RedirectResponse(url=google_auth_url)

@router.get("/auth/callback")
async def auth_google(request:Request,code: str,db: Session = Depends(get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URL,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=token_data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
 
    return user_info

