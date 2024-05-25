from datetime import timedelta
from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from livekit import api
from sqlalchemy.orm import Session

from api.utils.users import (
    create_user,
    edit_user,
    get_user,
    get_user_by_email,
    get_users,
)
from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from common.http_exceptions import MISSMATCHAUTH
from db.db_setup import get_db
from schemas.user import User, UserCreate, UserUpdate
from os import getenv
from dotenv import load_dotenv

router = fastapi.APIRouter()


@router.get("/users", response_model=List[User])
async def read_users(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/jwt", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise MISSMATCHAUTH
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.post("/users/me", response_model=User, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_user(db=db, user=user)


@router.put("/users/me", response_model=User)
async def update_user(
    user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return edit_user(db=db, user_id=current_user.id, user=user)


@router.get("/livekit/token")
async def get_livekit_token(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    load_dotenv()
    token = (
        api.AccessToken(
            api_key=getenv("LIVEKIT_API_KEY"), api_secret=getenv("LIVEKIT_API_SECRET")
        )
        .with_identity("python-bot")
        .with_name("Python Bot")
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room="my-room",
            )
        )
        .to_jwt()
    )
    return token

# TO_DO
# get /users/me/workspaces
