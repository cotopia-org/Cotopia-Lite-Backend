from sqlalchemy import Column, Integer, ForeignKey


from ..db_setup import Base
from .mixins import Timestamp
from sqlalchemy.orm import relationship


class PermissionRole(Timestamp, Base):
    __tablename__ = "permission_role"
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
    permission = relationship("Permission")
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    role = relationship("Role")
