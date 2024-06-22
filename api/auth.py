from datetime import timedelta

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse
# from authlib.integrations.starlette_client import OAuth,OAuthError
from settings import CLIENT_ID,CLIENT_SECRET


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

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

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

@router.get("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)
    
@router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return False
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return "movafaghiat amiz"

@router.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return "intended page"