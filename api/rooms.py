from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.room import (
    create_da_room,
    get_da_room_by_id,
    edit_da_room,
    delete_da_room,
)

from auth import get_current_active_user
from db.db_setup import get_db

from schemas.user import User
from schemas.room import Room, RoomCreate, RoomUpdate


router = fastapi.APIRouter()


@router.post("/room", response_model=Room, status_code=201)
async def create_room(
    room: RoomCreate,
    workspace_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_da_room(db=db, room=room, workspace_id=workspace_id)


@router.get("/room/{room_id}", response_model=Room)
async def get_room_by_id(
    room_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_room = get_da_room_by_id(db=db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail=f"Room (id = {room_id}) not found!")
    return db_room


@router.put("/room/{room_id}", response_model=Room, status_code=200)
async def update_room(
    room_id: int,
    room: RoomUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_room = get_da_room_by_id(db=db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail=f"Room (id = {room_id}) not found!")
    else:
        if True:  # check permission
            return edit_da_room(db=db, room_id=room_id, room=room)
        else:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action!",
            )


@router.delete("/room/{room_id}", status_code=204)
async def delete_room(
    room_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_room = get_da_room_by_id(db=db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail=f"Room (id = {room_id}) not found!")
    else:
        if True:  # check permission
            delete_da_room(db=db, room_id=room_id)
        else:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action!",
            )
