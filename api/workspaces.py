from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.workspace import create_ws, get_ws_by_id, edit_ws, delete_ws
from api.utils.room import get_da_rooms_by_workspace

from api.utils.auth import get_current_active_user
from db.db_setup import get_db

from schemas.user import User
from schemas.workspace import Workspace, WorkspaceCreate, WorkspaceUpdate
from schemas.room import Room

router = fastapi.APIRouter()


@router.post("/workspace", response_model=Workspace, status_code=201)
async def create_workspace(
        workspace: WorkspaceCreate,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    return create_ws(db=db, workspace=workspace, user_id=current_user.id)


@router.get("/workspace/{workspace_id}", response_model=Workspace)
async def get_workspace_by_id(
        workspace_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    db_workspace = get_ws_by_id(db=db, workspace_id=workspace_id)
    if db_workspace is None:
        raise HTTPException(
            status_code=404, detail=f"Workspace (id = {workspace_id}) not found!"
        )
    return db_workspace


@router.put("/workspace/{workspace_id}", response_model=Workspace, status_code=200)
async def update_workspace(
        workspace_id: int,
        workspace: WorkspaceUpdate,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    db_workspace = get_ws_by_id(db=db, workspace_id=workspace_id)
    if db_workspace is None:
        raise HTTPException(
            status_code=404, detail=f"Workspace (id = {workspace_id}) not found!"
        )
    else:
        if db_workspace.user_id == current_user.id:
            return edit_ws(db=db, workspace_id=workspace_id, workspace=workspace)
        else:
            raise HTTPException(
                status_code=403, detail="You are not the creator of this workspace!"
            )


@router.delete("/workspace/{workspace_id}", status_code=204)
async def delete_workspace(
        workspace_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    db_workspace = get_ws_by_id(db=db, workspace_id=workspace_id)
    if db_workspace is None:
        raise HTTPException(
            status_code=404, detail=f"Workspace (id = {workspace_id}) not found!"
        )
    else:
        if db_workspace.user_id == current_user.id:
            delete_ws(db=db, workspace_id=workspace_id)
        else:
            raise HTTPException(
                status_code=403, detail="You are not the creator of this workspace!"
            )


@router.get("/workspace/{workspace_id}/rooms", response_model=List[Room])
async def get_workspace_rooms(
        workspace_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    rooms = get_da_rooms_by_workspace(db=db, workspace_id=workspace_id)
    return rooms
