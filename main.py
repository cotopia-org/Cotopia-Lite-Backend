from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import auth, messages, rooms, users, workspaces, permissions, roles, lk, files
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

origins = ["https://lite-api.cotopia.social", "https://lite-api.cotopia.social/", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(SessionMiddleware, secret_key="add any string...")

# oauth = OAuth()
# oauth.register(
#     name='google',
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     client_kwargs={
#         'scope': 'email openid profile',
#         'redirect_url': 'http://localhost:8000/auth'
#     }
# )


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(workspaces.router)
app.include_router(rooms.router)
app.include_router(messages.router)
app.include_router(permissions.router)
app.include_router(roles.router)
app.include_router(lk.router)
app.include_router(files.router)
