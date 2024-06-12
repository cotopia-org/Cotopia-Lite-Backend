#  Room users status

import fastapi
from fastapi import WebSocket

router = fastapi.APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    def on(self, name, func):
        print(name)

        def decorator(*args, **kwargs):
            print(func, *args, **kwargs)
            func(*args, **kwargs)

        return decorator

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def receive_text(self, websocket: WebSocket):
        return await websocket.receive_text()

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# @router.websocket("/room_status/{room_id}")
# async def room_status(
#     room_id: int,
#     current_user: Annotated[User, Depends(get_current_active_user)],
#     websocket: WebSocket,
#     db: Session = Depends(get_db),
# ):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()
#
#             print("validation done!")
#
#             await manager.broadcast("Test")
#
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    @manager.on("Test")
    def test(name):
        print(name)

    test("HI")

    # await manager.connect(websocket)
    # while True:
    #     data = await manager.receive_text(websocket)
    #     await manager.send_personal_message(f"Message text was: {data}", websocket)
    #     print("Here")
