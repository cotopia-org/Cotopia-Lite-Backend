import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session

from api.utils.room import get_da_room_by_id
from db.db_setup import get_db
from db.models import Activity

router = fastapi.APIRouter()

from pydantic import BaseModel


class Participant(BaseModel):
    identity: str
    state: str | None = None


class Track(BaseModel):
    type: str
    name: str
    width: int
    height: int
    source: str
    mimeType: str
    stream: str


class Room(BaseModel):
    name: str


class Event(BaseModel):
    id: str
    event: str
    room: Room
    participant: Participant | None = None
    track: Track | None = None
    createdAt: int


@router.post("/livekit/events")
async def read_users(event: Event, db: Session = Depends(get_db)):

    # json = await request.json()
    # print(json)
    print(event)
    # print(request.headers)
    user_id = None
    state = None
    if event.participant is not None:
        user_id = int(event.participant.identity)
        state = event.participant.state

    room = get_da_room_by_id(db=db, room_id=int(event.room.name))

    db.add(
        Activity(
            user_id=user_id,
            room_id=room.id,
            workspace_id=room.workspace.id,
            event_type=event.event,
            event_id=event.id,
            state=state,
        )
    )

    db.commit()
