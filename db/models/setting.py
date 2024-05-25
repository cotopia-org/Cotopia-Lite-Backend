from sqlalchemy import Column, Integer, String, ForeignKey

from ..db_setup import Base
from .mixins import Timestamp


class Setting(Timestamp, Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    key = Column(String(63), nullable=False)
    value = Column(String(63), nullable=False)
