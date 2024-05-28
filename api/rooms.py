from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.room import create_da_room, get_da_room_by_id, edit_da_room, delete_da_room

from auth import get_current_active_user
from db.db_setup import get_db

from schemas.user import User
from schemas.room import Room, RoomCreate, RoomUpdate


router = fastapi.APIRouter()


@router.post("/room", response_model=Room, status_code=201)
async def create_room():
    pass

@router.get("/room/{room_id}", response_model=Room)
async def get_room_by_id():
    pass

@router.put("/room/{room_id}", response_model=Room, status_code=200)
async def update_room():
    pass


@router.delete("/room/{room_id}", status_code=204)
async def delete_room():
    pass