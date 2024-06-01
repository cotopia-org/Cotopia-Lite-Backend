from datetime import timedelta

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

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
