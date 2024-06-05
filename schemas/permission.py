from datetime import datetime

from pydantic import BaseModel


class PermissionBase(BaseModel):
    ability: str


class Permission(PermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    # permission_role

    class Config:
        orm_mode = True
