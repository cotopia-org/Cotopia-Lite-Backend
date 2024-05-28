from db.models.room_user import RoomUser as RoomUserModel
from sqlalchemy.orm import Session
import datetime
from schemas.room_user import RoomUserCreate, RoomUserUpdate


def create_ru(db: Session, room_user: RoomUserCreate, room_id: int, user_id: int):
    db_room_user = RoomUserModel(room_id=room_id, user_id=user_id)
    for var, value in vars(room_user).items():
        if value:
            setattr(db_room_user, var, value)
    db.add(db_room_user)
    db.commit()
    db.refresh(db_room_user)
    return db_room_user


def get_ru():
    pass


def edit_ru():
    pass


def delete_ru():
    pass

