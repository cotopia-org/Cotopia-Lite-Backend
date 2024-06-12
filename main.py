from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import auth, messages, rooms, users, workspaces, permissions, roles, lk, socket
from db.db_setup import Base, engine

Base.metadata.create_all(bind=engine)

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
            "url": "lite-api.cotopia.social",
            "description": "Staging environment",
        },
        {"url": "http://127.0.0.1:8000", "description": "Local environment"},
    ],
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(workspaces.router)
app.include_router(rooms.router)
app.include_router(messages.router)
app.include_router(permissions.router)
app.include_router(roles.router)
app.include_router(lk.router)
app.include_router(socket.router)
