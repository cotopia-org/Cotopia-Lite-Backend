from sqlalchemy.orm import Session

from db.models import UserWorkspace as UWRModel
from schemas.user_workspace import UserWorkspaceBase as UserWorkspaceRole


def create_uwr(db: Session, uwr: UserWorkspaceRole):
    db_uwr = UWRModel()
    for var, value in vars(uwr).items():
        if value:
            setattr(db_uwr, var, value)
    db.add(db_uwr)
    db.commit()
    db.refresh(db_uwr)
    return db_uwr


def get_uwr_by_id(db: Session, user_workspace_id: int):
    return db.query(UWRModel).filter(UWRModel.id == user_workspace_id).first()


def get_uwr(db: Session, user_id: int, workspace_id: int, role_id: int):
    return (
        db.query(UWRModel)
        .filter(
            UWRModel.user_id == user_id,
            UWRModel.workspace_id == workspace_id,
            UWRModel.role_id == role_id,
        )
        .first()
    )


def get_uwr_by_user(db: Session, user_id: int):
    return db.query(UWRModel).filter(UWRModel.user_id == user_id).all()


def get_uwr_by_user_workspace(db: Session, user_id: int, workspace_id: int):
    return (
        db.query(UWRModel)
        .filter(UWRModel.user_id == user_id, UWRModel.workspace_id == workspace_id)
        .all()
    )


def get_uwr_by_user_role(db: Session, user_id: int, role_id: int):
    return (
        db.query(UWRModel)
        .filter(UWRModel.user_id == user_id, UWRModel.role_id == role_id)
        .all()
    )


def get_uwr_by_workspace(db: Session, workspace_id: int):
    return db.query(UWRModel).filter(UWRModel.workspace_id == workspace_id).all()


def get_uwr_by_workspace_role(db: Session, workspace_id: int, role_id: int):
    return (
        db.query(UWRModel)
        .filter(UWRModel.workspace_id == workspace_id, UWRModel.role_id == role_id)
        .all()
    )


def get_uwr_by_role(db: Session, role_id: int):
    return db.query(UWRModel).filter(UWRModel.role_id == role_id).all()


def delete_uwr(db: Session, user_id: int, workspace_id: int, role_id: int):
    db_uwr = (
        db.query(UWRModel)
        .filter(
            UWRModel.user_id == user_id,
            UWRModel.workspace_id == workspace_id,
            UWRModel.role_id == role_id,
        )
        .first()
    )
    db.delete(db_uwr)
    db.commit()
    return db_uwr


def delete_uwr_by_id(db: Session, user_workspace_id: int):
    db_uwr = db.query(UWRModel).get(user_workspace_id)
    db.delete(db_uwr)
    db.commit()
    return db_uwr
