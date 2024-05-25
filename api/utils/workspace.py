from db.models.workspace import Workspace as WorkspaceModel
from sqlalchemy.orm import Session
from schemas.workspace import WorkspaceCreate, WorkspaceUpdate
import datetime


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
