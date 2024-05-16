import enum as pyEnum

from sqlalchemy import Boolean, Column, Enum, Integer, String

from ..db_setup import Base
from .mixins import Timestamp


class Role(pyEnum.IntEnum):
    default = 1


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(511))
    role = Column(Enum(Role), nullable=False, default=1)
    is_active = Column(Boolean, default=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
