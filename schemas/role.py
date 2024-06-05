from datetime import datetime

from pydantic import BaseModel


class RoleBase(BaseModel):
    title: str
    description: str


class Role(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    # user_workspace: UserWorkspace
    # permission_role

    class Config:
        orm_mode = True
