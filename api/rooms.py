from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.auth import get_current_active_user
from api.utils.helpers import error
from api.utils.room import (create_da_room, delete_da_room, edit_da_room,
                            get_da_room_by_id)
from db.db_setup import get_db
from db.models import RoomUser
from schemas.message import Message
from schemas.room import Room, RoomCreate, RoomUpdate
from schemas.user import User

router = fastapi.APIRouter()


@router.post("/room", response_model=Room, status_code=201)
async def create_room(
        room: RoomCreate,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    return create_da_room(db=db, room=room, workspace_id=room.workspace_id)


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


@router.get("/rooms/{room_id}/users", response_model=List[User])
async def get_room_users(
        room_id: int,
        db: Session = Depends(get_db),
):
    users = []
    room = get_da_room_by_id(db=db, room_id=room_id)
    for room_user in room.room_user:
        users.append(room_user.user)

    return users


@router.get("/rooms/{room_id}/join", response_model=Room)
async def join_workspace_by_id(
        room_id: int,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    room = get_da_room_by_id(db=db, room_id=room_id)

    room_user = db.query(RoomUser).filter(RoomUser.room_id == room_id,
                                          RoomUser.user_id == user.id).first()
    if room_user is None:
        room_user = RoomUser(user_id=user.id, room_id=room_id)

        db.add(room_user)
        db.commit()
        return room

    return error('You are already in this room')


@router.get("/rooms/{room_id}/leave", response_model=Room)
async def leave_room_by_id(
        room_id: int,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    room = get_da_room_by_id(db=db, room_id=room_id)

    room_user = db.query(RoomUser).filter(RoomUser.room_id == room_id,
                                          RoomUser.user_id == user.id).first()
    if room_user is not None:
        db.query(RoomUser).filter_by(id=room_user.id).delete()
        db.commit()
        return room

    return error('You are not in this room')


@router.get("/rooms/{room_id}/messages", response_model=List[Message])
async def get_room_users(
        room_id: int,
        db: Session = Depends(get_db),
):
    messages = []
    room = get_da_room_by_id(db=db, room_id=room_id)

    for message in room.messages:
        print(message.user)
    return room.messages
