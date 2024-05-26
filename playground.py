from os import getenv
from dotenv import load_dotenv
from livekit import api
import asyncio


async def main():
    load_dotenv()
    lkapi = api.LiveKitAPI(
        url=getenv("LIVEKIT_API_URL"),
        api_key=getenv("LIVEKIT_API_KEY"),
        api_secret=getenv("LIVEKIT_API_SECRET"),
    )
    room_info = await lkapi.room.create_room(
        api.CreateRoomRequest(name="my-room"),
    )
    print(room_info)
    results = await lkapi.room.list_rooms(api.ListRoomsRequest())
    print(results)
    await lkapi.aclose()


asyncio.get_event_loop().run_until_complete(main())
