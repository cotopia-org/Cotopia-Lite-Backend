import datetime

from sqlalchemy.orm import Session

from db.models import Message as MessageModel
from schemas.message import MessageCreate, MessageUpdate


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


def get_msg_by_id(db: Session, message_id: int):
    return db.query(MessageModel).filter(MessageModel.id == message_id).first()


def edit_msg(db: Session, message_id: int, message: MessageUpdate):
    db_msg = db.query(MessageModel).get(message_id)
    db_msg.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db_msg.edited = True

    for var, value in vars(message).items():
        if value:
            setattr(db_msg, var, value)

    db.add(db_msg)
    db.commit()
    return db_msg


def delete_msg(db: Session, message_id: int):
    db_msg = db.query(MessageModel).get(message_id)
    db.delete(db_msg)
    db.commit()
    return db_msg
