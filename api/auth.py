from datetime import timedelta
from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.utils.user import (
    create_user,
    edit_user,
    get_user,
    get_user_by_email,
    get_users,
)
from api.utils.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from api.utils.auth import get_user as get_user_by_username
from common.http_exceptions import MISSMATCHAUTH
from db.db_setup import get_db
from schemas.user import User, UserCreate, UserUpdate

router = fastapi.APIRouter()


@router.post("/auth/login", response_model=Token)
async def login(
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
    return {"access_token": access_token, "token_type": "bearer", user: user}


@router.post("/auth/register", response_model=User, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username is already registered")
    return create_user(db=db, user=user)
