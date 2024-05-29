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


@router.delete("/leave_room", status_code=204)
async def delete_room(
    room_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_room_user = get_ru(db=db, room_id=room_id, user_id=current_user.id)
    if db_room_user is None:
        raise HTTPException(status_code=404, detail=f"RoomUser (room_id = {room_id}, user_id = {current_user.id}) not found!")
    else:
        if True:  # check permission
            delete_ru(db=db, room_id=room_id, user_id=current_user.id)
        else:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action!",
            )


#  Room users status