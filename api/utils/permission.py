import datetime

from sqlalchemy.orm import Session

from db.models import Permission as PermissionModel
from schemas.permission import PermissionBase


def create_da_permission(db: Session, permission: PermissionBase):
    db_permission = PermissionModel()
    for var, value in vars(permission).items():
        if value:
            setattr(db_permission, var, value)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def get_da_role_by_id(db: Session, role_id: int):
    return db.query(RoleModel).filter(RoleModel.id == role_id).first()


def edit_da_role(db: Session, role_id: int, role: RoleBase):
    db_role = db.query(RoleModel).get(role_id)
    db_role.updated_at = datetime.datetime.now(datetime.timezone.utc)

    for var, value in vars(role).items():
        if value:
            setattr(db_role, var, value)

    db.add(db_role)
    db.commit()
    return db_role


def delete_da_role(db: Session, role_id: int):
    db_role = db.query(RoleModel).get(role_id)
    db.delete(db_role)
    db.commit()
    return db_role
