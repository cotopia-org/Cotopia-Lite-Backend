from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.models.permission import Permission  # noqa: F401
from db.models.role import Role  # noqa: F401

from ..db_setup import Base
from .mixins import Timestamp


class PermissionRole(Timestamp, Base):
    __tablename__ = "permission_role"
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
    permission = relationship("Permission")
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    role = relationship("Role")
