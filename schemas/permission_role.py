from datetime import datetime

from pydantic import BaseModel

from schemas.permission import Permission
from schemas.role import Role


class PermissionRoleBase(BaseModel):
    permission_id: int
    role_id: int


class PermissionRole(PermissionRoleBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    permission: Permission
    role: Role

    class Config:
        orm_mode = True
