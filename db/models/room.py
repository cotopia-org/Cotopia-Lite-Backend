from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.models.message import Message  # noqa: F401

from ..db_setup import Base
from .mixins import Timestamp


class Room(Timestamp, Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    passcode = Column(String(15), nullable=True)
    title = Column(String(50), nullable=True)
    status = Column(String(31), nullable=True)
    avatar = Column(String(255), nullable=True)
    background_image = Column(String(255), nullable=True)
    landing_spot = Column(String(31), nullable=True, default="0, 0")
    messages = relationship("Message")
