from db.models.room import Room as RoomModel
from sqlalchemy.orm import Session
import datetime
from schemas.room import RoomCreate, RoomUpdate



def create_da_room(db: Session, room: RoomCreate, workspace_id: int):
    db_room = RoomModel(workspace_id=workspace_id)
    for var, value in vars(room).items():
        if value:
            setattr(db_room, var, value)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_da_room_by_id(db: Session, room_id: int):
    return db.query(RoomModel).filter(RoomModel.id == room_id).first()

def get_da_rooms_by_workspace(db: Session, workspace_id: int):
    return db.query(RoomModel).filter(RoomModel.workspace_id == workspace_id).all()

def edit_da_room():
    pass

def delete_da_room():
    pass