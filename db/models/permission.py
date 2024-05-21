from sqlalchemy import Column, Integer, String

from ..db_setup import Base
from .mixins import Timestamp


class Permission(Timestamp, Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    ability = Column(String(63), nullable=False)
