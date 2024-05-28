from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.room_user import create_ru, get_ru, edit_ru, delete_ru
from auth import get_current_active_user
from db.db_setup import get_db

from schemas.user import User
from schemas.room_user import RoomUserCreate, RoomUserUpdate


router = fastapi.APIRouter()

# Joining the room

# Leaving the room

#  Room users status