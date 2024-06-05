from datetime import datetime

from pydantic import BaseModel

from schemas.user import User
from schemas.workspace import Workspace


class UserWorkspaceBase(BaseModel):
    user_id: int
    workspace_id: int
    role_id: int


class UserWorkspace(UserWorkspaceBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    user: User
    workspace: Workspace
    # role: Role

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    title: str
    description: str


class Role(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    user_workspace: UserWorkspace
    # permission_role

    class Config:
        orm_mode = True


class PermissionBase(BaseModel):
    ability: str


class Permission(PermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    # permission_role

    class Config:
        orm_mode = True


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
