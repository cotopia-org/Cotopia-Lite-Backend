from datetime import datetime

from pydantic import BaseModel

from schemas.user import User
from schemas.workspace import Workspace
from schemas.role import Role


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
    role: Role

    class Config:
        orm_mode = True
