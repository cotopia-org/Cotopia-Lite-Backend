from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.auth import get_current_active_user
from api.utils.helpers import error
from api.utils.room import get_da_rooms_by_workspace
from api.utils.workspace import create_ws, delete_ws, edit_ws, get_ws_by_id
from db.db_setup import get_db
from db.models import UserWorkspace
from db.models import Workspace as WorkspaceModel
from schemas.room import Room
from schemas.user import User
from schemas.workspace import Workspace, WorkspaceCreate, WorkspaceUpdate

router = fastapi.APIRouter()


@router.post("/workspaces/create", response_model=Workspace, status_code=201)
async def create_workspace(
        workspace: WorkspaceCreate,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    db_ws = (
        db.query(WorkspaceModel).filter(WorkspaceModel.name == workspace.name).first()
    )
    if db_ws:
        raise HTTPException(
            status_code=400, detail="There is another workspace with this name."
        )
    return create_ws(db=db, workspace=workspace, user_id=current_user.id)


@router.get("/workspaces/{workspace_id}", response_model=Workspace)
async def get_workspace_by_id(
        workspace_id: int,
        db: Session = Depends(get_db),
):
    db_workspace = get_ws_by_id(db=db, workspace_id=workspace_id)
    if db_workspace is None:
        raise HTTPException(
            status_code=404, detail=f"Workspace (id = {workspace_id}) not found!"
        )
    return db_workspace


@router.put("/workspaces/{workspace_id}/update", response_model=Workspace, status_code=200)
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


@router.delete("/workspaces/{workspace_id}/delete", status_code=204)
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


@router.get("/workspaces/{workspace_id}/rooms", response_model=List[Room])
async def get_workspace_rooms(
        workspace_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    rooms = get_da_rooms_by_workspace(db=db, workspace_id=workspace_id)
    return rooms


@router.get("/workspaces/{workspace_id}/join", response_model=Workspace)
async def join_workspace_by_id(
        workspace_id: int,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    workspace = get_ws_by_id(db=db, workspace_id=workspace_id)

    user_workspace = db.query(UserWorkspace).filter(UserWorkspace.workspace_id == workspace_id,
                                                    UserWorkspace.user_id == user.id).first()
    if user_workspace is None:
        user_workspace = UserWorkspace(user_id=user.id, workspace_id=workspace.id)

        db.add(user_workspace)
        db.commit()
        return workspace

    return error('You are already in this workspace')


@router.get("/workspaces/{workspace_id}/leave", response_model=Workspace)
async def leave_workspace_by_id(
        workspace_id: int,
        user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    workspace = get_ws_by_id(db=db, workspace_id=workspace_id)

    user_workspace = db.query(UserWorkspace).filter(UserWorkspace.workspace_id == workspace_id,
                                                    UserWorkspace.user_id == user.id).first()
    if user_workspace is not None:
        db.query(UserWorkspace).filter_by(id=user_workspace.id).delete()
        db.commit()
        return workspace

    return error('You are not in this workspace')


@router.get("/workspaces/{workspace_id}/users", response_model=List[User])
async def get_workspace_users(
        workspace_id: int,
        db: Session = Depends(get_db),
):
    users = []
    workspace = get_ws_by_id(db=db, workspace_id=workspace_id)
    for user_workspace in workspace.user_workspace:
        users.append(user_workspace.user)

    return users
