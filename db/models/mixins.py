import datetime
from datetime import timezone

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now(timezone.utc), nullable=False)
