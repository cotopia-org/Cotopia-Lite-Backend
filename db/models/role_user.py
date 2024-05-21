from sqlalchemy import Column, Integer, ForeignKey


from ..db_setup import Base
from .mixins import Timestamp
from sqlalchemy.orm import relationship


class RoleUser(Timestamp, Base):
    __tablename__ = "role_user"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User")
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    role = relationship("Role")
