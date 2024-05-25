from db.models.workspace import Workspace as WorkspaceModel
from sqlalchemy.orm import Session
from schemas.workspace import WorkspaceCreate


def create_ws(db: Session, workspace: WorkspaceCreate, user_id: int):
    db_workspace = WorkspaceModel(user_id=user_id)
    for var, value in vars(workspace).items():
        if value:
            setattr(db_workspace, var, value)
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace


def get_ws():
    pass


def edit_ws():
    pass


def delete_ws():
    pass
