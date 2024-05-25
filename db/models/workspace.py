from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from ..db_setup import Base
from .mixins import Timestamp
from sqlalchemy.orm import relationship


class Workspace(Timestamp, Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_private = Column(Boolean, default=False)
    avatar = Column(String(255), nullable=True)
    banner = Column(String(255), nullable=True)
    rooms = relationship("Room")
    settingd = relationship("Setting")
