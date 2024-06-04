from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.auth import get_current_active_user
from api.utils.message import create_msg, get_room_msgs, edit_msg, delete_msg
from db.db_setup import get_db
from db.models import Message as MessageModel
from schemas.message import Message, MessageCreate
from schemas.user import User

router = fastapi.APIRouter()


@router.post("/messages/send", response_model=Message, status_code=201)
async def send_message(
    room_id: int,
    message: MessageCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_msg(db=db, message=message, user_id=current_user.id, room_id=room_id)