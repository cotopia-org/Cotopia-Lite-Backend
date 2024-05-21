from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from enum import Enum as pyEnum


from ..db_setup import Base
from .mixins import Timestamp
from sqlalchemy.orm import relationship


class VoiceStatus(pyEnum):
    disconnected = "disconnected"
    muted = "muted"
    unmuted = "unmuted"
    deafened = "deafened"


class VideoStatus(pyEnum):
    disconnected = "disconnected"
    camera = "sharing camera"
    screen = "sharing screen"


class RoomUser(Timestamp, Base):
    __tablename__ = "room_user"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User")
    room_id = Column(Integer, ForeignKey("rooms.id"), primary_key=True)
    room = relationship("Room")
    voice_status = Column(
        Enum(VoiceStatus), nullable=False, default=VoiceStatus.disconnected
    )
    video_status = Column(
        Enum(VideoStatus), nullable=False, default=VideoStatus.disconnected
    )
    coordinates = Column(String(31), nullable=False, default="0, 0")
