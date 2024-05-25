from sqlalchemy import Boolean, Column, Integer, ForeignKey, Text

from ..db_setup import Base
from .mixins import Timestamp


class Message(Timestamp, Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    reply_to = Column(Integer, nullable=True)
    edited = Column(Boolean, default=False)
    text = Column(Text)
