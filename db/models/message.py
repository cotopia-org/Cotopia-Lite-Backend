from sqlalchemy import Boolean, Column, Integer, ForeignKey, Text

from ..db_setup import Base
from .mixins import Timestamp
from sqlalchemy.orm import relationship


class Message(Timestamp, Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User")
    room_id = Column(Integer, ForeignKey("rooms.id"), primary_key=True)
    room = relationship("Room")
    reply_to = Column(Integer, nullable=True)
    edited = Column(Boolean, default=False)
    text = Column(Text(2047))
