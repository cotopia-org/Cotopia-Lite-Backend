from enum import Enum as pyEnum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


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
    is_active = Column(Boolean, default=True)
    voice_status = Column(
        Enum(VoiceStatus), nullable=False, default=VoiceStatus.disconnected
    )
    video_status = Column(
        Enum(VideoStatus), nullable=False, default=VideoStatus.disconnected
    )
    coordinates = Column(String(31), nullable=False, default="0, 0")
    screenshare_coordinates = Column(String(31), nullable=False, default="0, 0")
    screenshare_size = Column(String(31), nullable=False, default="0, 0")
    video_coordinates = Column(String(31), nullable=False, default="0, 0")
    video_size = Column(String(31), nullable=False, default="0, 0")
