from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.auth import get_current_active_user
from api.utils.message import create_msg, get_room_msgs, edit_msg, delete_msg, get_msg_by_id
from db.db_setup import get_db
from db.models import Message as MessageModel
from schemas.message import Message, MessageCreate, MessageUpdate
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


@router.get("/messages", response_model=List[Message])
async def get_messages(
    room_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    messages = get_room_msgs(db=db, room_id=room_id, skip=skip, limit=limit)
    return messages


@router.put("/messages/{message_id}/update", response_model=Message, status_code=200)
async def edit_message(
    message_id: int,
    message: MessageUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_message = get_msg_by_id(db=db, message_id=message_id)
    if db_message is None:
        raise HTTPException(
            status_code=404, detail=f"Message (id = {message_id}) not found!"
        )
    else:
        if db_message.user_id == current_user.id:
            return edit_msg(db=db, message_id=message_id, message=message)
        else:
            raise HTTPException(
                status_code=403, detail="You are not the author of this message!"
            )


@router.delete("/messages/{message_id}/delete", status_code=204)
async def delete_message(
    message_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_message = get_msg_by_id(db=db, message_id=message_id)
    if db_message is None:
        raise HTTPException(
            status_code=404, detail=f"Message (id = {message_id}) not found!"
        )
    else:
        if db_message.user_id == current_user.id:
            delete_msg(db=db, message_id=message_id)
        else:
            raise HTTPException(
                status_code=403, detail="You are not the author of this message!"
            )