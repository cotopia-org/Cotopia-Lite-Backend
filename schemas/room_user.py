from datetime import datetime

from pydantic import BaseModel, ConfigDict

from db.models import VoiceStatus, VideoStatus


class RoomUserBase(BaseModel):
    user_id: int
    room_id: int


class RoomUserCreate(RoomUserBase):
    voice_status: VoiceStatus
    video_status: VideoStatus
    coordinates: str | None = None


class RoomUserUpdate(RoomUserCreate):
    model_config = ConfigDict(validate_assignment=True)
    voice_status: VoiceStatus | None = None
    video_status: VideoStatus | None = None
    coordinates: str | None = None
    screenshare_coordinates: str | None = None
    screenshare_size: str | None = None
    video_coordinates: str | None = None
    video_size: str | None = None


class RoomUser(RoomUserUpdate):
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
