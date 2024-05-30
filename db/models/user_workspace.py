from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class UserWorkspace(Timestamp, Base):
    __tablename__ = "user_workspace"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User")
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), primary_key=True)
    workspace = relationship("Room")
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    role = relationship("Role")
