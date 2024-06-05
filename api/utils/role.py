import datetime

from sqlalchemy.orm import Session

from db.models import Role as RoleModel
from schemas.role import RoleBase, Role


def create_da_role(db: Session, role: RoleBase):
    db_role = RoleModel()
    for var, value in vars(role).items():
        if value:
            setattr(db_role, var, value)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_da_room_by_id(db: Session, room_id: int):
    return db.query(RoomModel).filter(RoomModel.id == room_id).first()


def get_da_rooms_by_workspace(db: Session, workspace_id: int):
    return db.query(RoomModel).filter(RoomModel.workspace_id == workspace_id).all()


def edit_da_room(db: Session, room_id: int, room: RoomUpdate):
    db_room = db.query(RoomModel).get(room_id)
    db_room.updated_at = datetime.datetime.now(datetime.timezone.utc)

    for var, value in vars(room).items():
        if value:
            setattr(db_room, var, value)

    db.add(db_room)
    db.commit()
    return db_room


def delete_da_room(db: Session, room_id: int):
    db_room = db.query(RoomModel).get(room_id)
    db_room.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db_room.is_active = False

    db.add(db_room)
    db.commit()
    return db_room
