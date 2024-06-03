from datetime import datetime

from pydantic import BaseModel


class RoomBase(BaseModel):
    workspace_id: int


class RoomCreate(RoomBase):
    title: str


class RoomUpdate(RoomCreate):
    title: str | None = None
    status: str | None = None
    is_locked: bool | None = None
    passcode: str | None = None
    avatar: str | None = None
    background_image: str | None = None
    landing_spot: str | None = None


class Room(RoomUpdate):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
