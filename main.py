from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import users, workspaces
from db.db_setup import engine
from db.models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Live Kit API",
    description="Just a test",
    version="0.42",
    contact={
        "name": "Ali Kharrati",
        "email": "ali.kharrati@gmail.com",
    },
    servers=[
        {
            "url": "https://livekit-api.cotopia.social",
            "description": "Staging environment",
        },
        {"url": "http://127.0.0.1:8000", "description": "Local environment"},
    ],
)

origins = ["https://livekit-api.cotopia.social", "https://livekit-api.cotopia.social/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(workspaces.router)
