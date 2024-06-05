from sqlalchemy.orm import Session

from db.models import PermissionRole as PRModel
from schemas.permission_role import PermissionRoleBase


def create_da_pr(db: Session, permission_role: PermissionRoleBase):
    db_permission_role = PRModel()
    for var, value in vars(permission_role).items():
        if value:
            setattr(db_permission_role, var, value)
    db.add(db_permission_role)
    db.commit()
    db.refresh(db_permission_role)
    return db_permission_role


def get_da_pr_by_id(db: Session, permission_role_id: int):
    return db.query(PRModel).filter(PRModel.id == permission_role_id).first()


def get_da_pr(db: Session, permission_id: int, role_id: int):
    return (
        db.query(PRModel)
        .filter(PRModel.permission_id == permission_id, PRModel.role_id == role_id)
        .first()
    )


def delete_da_pr(db: Session, permission_role_id: int):
    db_permission_role = db.query(PRModel).get(permission_role_id)
    db.delete(db_permission_role)
    db.commit()
    return db_permission_role
