from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.room_user import create_ru, get_ru, edit_ru, delete_ru
from auth import get_current_active_user
from db.db_setup import get_db

from schemas.user import User
from schemas.room_user import RoomUserCreate, RoomUserUpdate, RoomUser


router = fastapi.APIRouter()


@router.post("/join_room", response_model=RoomUser, status_code=201)
async def join_room(
    room_user: RoomUserCreate,
    room_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_ru(db=db, room_user=room_user, room_id=room_id, user_id=current_user.id)

# Leaving the room

#  Room users status