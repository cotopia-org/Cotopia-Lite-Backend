from datetime import datetime

from pydantic import BaseModel

class WorkspaceBase(BaseModel):
    user_id: int
    

class WorkspaceCreate(WorkspaceBase):
    name: str

class WorkspaceUpdate(WorkspaceCreate):
    name: str | None = None
    description: str | None = None
    is_private: bool | None = None
    avatar: str | None = None
    banner: str | None = None

class Workspace(WorkspaceUpdate):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True