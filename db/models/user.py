from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from db.models.message import Message  # noqa: F401
from db.models.workspace import Workspace  # noqa: F401

from ..db_setup import Base
from .mixins import Timestamp


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(511))
    is_active = Column(Boolean, default=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(63), nullable=True)
    status = Column(String(31), nullable=True)
    avatar = Column(String(255), nullable=True)
    bio = Column(String(255), nullable=True)
    workspaces = relationship("Workspace")
    messages = relationship("Message")
