from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from ..db_setup import Base
from .mixins import Timestamp
from sqlalchemy.orm import relationship


class Room(Timestamp, Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    workspace = relationship("Workspace")
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    passcode = Column(String(15), nullable=True)
    title = Column(String(50), nullable=True)
    status = Column(String(31), nullable=True)
    avatar = Column(String(255), nullable=True)
    background_image = Column(String(255), nullable=True)
