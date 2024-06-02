from pydantic import BaseModel

from schemas.room import Room
from schemas.user import User


class MessageBase(BaseModel):
    id: int


class Message(MessageBase):
    user_id: int
    user: User

    room_id: int
    room: Room

    reply_to: int | None

    edited: bool
    text: str

    class Config:
        orm_mode = True
