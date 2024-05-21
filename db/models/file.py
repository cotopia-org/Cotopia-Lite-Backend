from sqlalchemy import Column, Integer, String

from ..db_setup import Base
from .mixins import Timestamp


class File(Timestamp, Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    fillable_id = Column(Integer, nullable=False)
    fillable_type = Column(String(31), nullable=False)
    mime_type = Column(String(31), nullable=False)
    path = Column(String(255), nullable=False)
