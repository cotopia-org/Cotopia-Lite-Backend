from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.workspace import create_ws, get_ws_by_id, get_ws_by_user, edit_ws, delete_ws

from auth import get_current_active_user
from db.db_setup import get_db

from schemas.user import User
from schemas.workspace import Workspace, WorkspaceCreate, WorkspaceUpdate



router = fastapi.APIRouter()


@router.post("/workspace", response_model=Workspace, status_code=201)
async def create_workspace(workspace: WorkspaceCreate,
                           current_user: Annotated[User, Depends(get_current_active_user)],
                           db: Session = Depends(get_db),
                           ):
    return create_ws(db=db, workspace=workspace, user_id=current_user.id)


@router.get("/workspace/{workspace_id}", response_model=Workspace)
async def get_workspace_by_id():
    pass


@router.put("/workspace/{workspace_id}", response_model=Workspace, status_code=200)
async def update_workspace():
    pass

@router.delete("/workspace/{workspace_id}", response_model=Workspace, status_code=204)
async def delete_workspace():
    pass