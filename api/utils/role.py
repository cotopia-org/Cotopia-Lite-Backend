import datetime

from sqlalchemy.orm import Session

from db.models import Role as RoleModel
from schemas.role import RoleBase


def create_da_role(db: Session, role: RoleBase):
    db_role = RoleModel()
    for var, value in vars(role).items():
        if value:
            setattr(db_role, var, value)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


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
