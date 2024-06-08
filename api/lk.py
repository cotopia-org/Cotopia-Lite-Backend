import fastapi

router = fastapi.APIRouter()

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@router.post("/livekit/events")
async def read_users(request: fastapi.Request):
    json = await request.json()
    print(json)
