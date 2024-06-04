from datetime import datetime

from pydantic import BaseModel

from schemas.room import Room
from schemas.user import User


class MessageBase(BaseModel):
    user_id: int
    room_id: int


class MessageCreate(MessageBase):
    text: str
    reply_to: int | None = None


class MessageUpdate(MessageBase):
    text: str


class Message(MessageBase):
    id: int
    user: User
    room: Room
    edited: bool
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
