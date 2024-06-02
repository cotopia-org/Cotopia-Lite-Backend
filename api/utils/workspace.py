import datetime

from sqlalchemy.orm import Session

from api.utils.helpers import error
from db.models import User
from db.models import Workspace as WorkspaceModel
from schemas.workspace import WorkspaceCreate, WorkspaceUpdate


def get_all_workspaces(db: Session, workspace_id: int):
    return db.query(WorkspaceModel).all()


def get_user_workspaces(user: User):
    workspaces = []
    for user_workspace in user.user_workspace:
        workspaces.append(user_workspace.workspace)

    return workspaces


def create_ws(db: Session, workspace: WorkspaceCreate, user_id: int):
    db_workspace = WorkspaceModel(user_id=user_id)
    for var, value in vars(workspace).items():
        if value:
            setattr(db_workspace, var, value)
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace


def get_ws_by_id(db: Session, workspace_id: int):
    ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == workspace_id).first()
    if ws is None:
        return error('Workspace not found', 404)
    return ws


def get_ws_by_user(db: Session, user_id: int):
    return db.query(WorkspaceModel).filter(WorkspaceModel.user_id == user_id).all()


def edit_ws(db: Session, workspace_id: int, workspace: WorkspaceUpdate):
    db_workspace = db.query(WorkspaceModel).get(workspace_id)
    db_workspace.updated_at = datetime.datetime.now(datetime.timezone.utc)

    for var, value in vars(workspace).items():
        if value:
            setattr(db_workspace, var, value)

    db.add(db_workspace)
    db.commit()
    return db_workspace


def delete_ws(db: Session, workspace_id: int):
    db_workspace = db.query(WorkspaceModel).get(workspace_id)
    db_workspace.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db_workspace.is_active = False

    db.add(db_workspace)
    db.commit()
    return db_workspace
