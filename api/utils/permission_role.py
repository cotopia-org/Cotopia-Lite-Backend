import datetime

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


def get_da_role_by_id(db: Session, role_id: int):
    return db.query(RoleModel).filter(RoleModel.id == role_id).first()




def delete_da_role(db: Session, role_id: int):
    db_role = db.query(RoleModel).get(role_id)
    db.delete(db_role)
    db.commit()
    return db_role
