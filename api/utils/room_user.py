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


def get_ru(db: Session, room_id: int, user_id: int):
    return db.query(RoomUserModel).filter(RoomUserModel.room_id == room_id, RoomUserModel.user_id == user_id).first()


def edit_ru(db: Session, room_id: int, user_id: int, room_user: RoomUserUpdate):
    db_room_user = db.query(RoomUserModel).get({"room_id": room_id, "user_id": user_id})
    db_room_user.updated_at = datetime.datetime.now(datetime.timezone.utc)

    for var, value in vars(room_user).items():
        if value:
            setattr(db_room_user, var, value)

    db.add(db_room_user)
    db.commit()
    return db_room_user


def delete_ru(db: Session, room_id: int, user_id: int):
    db_room_user = db.query(RoomUserModel).get({"room_id": room_id, "user_id": user_id})
    db_room_user.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db_room_user.is_active = False

    db.add(db_room_user)
    db.commit()
    return db_room_user
