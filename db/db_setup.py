from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DATABASE')}"
# ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://gwen@localhost/fast_lms"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)
# async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
# AsyncSessionLocal = sessionmaker(
#     async_engine, class_=AsyncSession, expire_on_commit=False
# )

Base = declarative_base()


# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def async_get_db():
#     async with AsyncSessionLocal() as db:
#         yield db
#         await db.commit()
