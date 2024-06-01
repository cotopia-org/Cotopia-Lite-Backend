import datetime

from sqlalchemy.orm import Session

from db.models import UserWorkspace
from db.models import Workspace as WorkspaceModel
from schemas.workspace import WorkspaceCreate, WorkspaceUpdate


def get_all_workspaces(db: Session, workspace_id: int):
    return db.query(WorkspaceModel).all()


def get_user_workspaces(db: Session, user_id: int):
    user_workspaces = db.query(UserWorkspace).filter(UserWorkspace.user_id == user_id).all()
    workspaces = []
    for user_worksapce in user_workspaces:
        workspaces.append(user_worksapce.workspace)

    return workspaces
    # return db.query(WorkspaceModel).all()


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
    return db.query(WorkspaceModel).filter(WorkspaceModel.id == workspace_id).first()


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
