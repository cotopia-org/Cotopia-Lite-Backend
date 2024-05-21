from sqlalchemy import Boolean, Column, Integer, String

from ..db_setup import Base
from .mixins import Timestamp


class User(Timestamp, Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    passcode = Column(String(15), nullable=True)
    title = Column(String(50), nullable=True)
    status = Column(String(31), nullable=True)
    avatar = Column(String(255), nullable=True)
    background_image = Column(String(255), nullable=True)
