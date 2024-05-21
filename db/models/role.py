from sqlalchemy import Column, Integer, String

from ..db_setup import Base
from .mixins import Timestamp


class Role(Timestamp, Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(63), nullable=True)
    description = Column(String(255), nullable=True)
