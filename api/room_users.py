import time
from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from api.utils.room_user import create_ru, delete_ru, edit_ru, get_ru
from api.utils.auth import get_current_active_user
from db.db_setup import get_db
from schemas.room_user import RoomUser, RoomUserCreate, RoomUserUpdate
from schemas.user import User

router = fastapi.APIRouter()


@router.post("/room/{room_id}/join", response_model=RoomUser, status_code=201)
async def join_room(
        room_user: RoomUserCreate,
        room_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    return create_ru(
        db=db, room_user=room_user, room_id=room_id, user_id=current_user.id
    )


@router.delete("/room/{room_id}/leave", status_code=204)
async def delete_room(
        room_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    db_room_user = get_ru(db=db, room_id=room_id, user_id=current_user.id)
    if db_room_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"RoomUser (room_id = {room_id}, user_id = {current_user.id}) not found!",
        )
    else:
        if True:  # check permission
            delete_ru(db=db, room_id=room_id, user_id=current_user.id)
        else:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action!",
            )


@router.put("/room/{room_id}/updateStatus", response_model=RoomUser, status_code=200)
async def update_ru(
        room_id: int,
        room_user: RoomUserUpdate,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    # TO-DO
    # Change status of others based on role
    db_room_user = get_ru(db=db, room_id=room_id, user_id=current_user.id)
    if db_room_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"RoomUser (room_id = {room_id}, user_id = {current_user.id}) not found!",
        )
    else:
        if True:  # check permission
            return edit_ru(
                db=db, room_id=room_id, user_id=current_user.id, room_user=room_user
            )
        else:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action!",
            )


#  Room users status


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/room_status/{room_id}")
async def room_status(room_id: int, websocket: WebSocket, room_user: RoomUserUpdate):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
            time.sleep(10)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/test")
async def test(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
            time.sleep(10)
    except WebSocketDisconnect:
        manager.disconnect(websocket)