from sqlalchemy.orm import Session

from db.models import Message as MessageModel
from schemas.message import MessageCreate


def create_msg(db: Session, message: MessageCreate, user_id: int, room_id: int):
    db_msg = MessageModel(user_id=user_id, room_id=room_id)
    for var, value in vars(message).items():
        if value:
            setattr(db_msg, var, value)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


def get_room_msgs(db: Session, room_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(MessageModel)
        .filter(MessageModel.room_id == room_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
