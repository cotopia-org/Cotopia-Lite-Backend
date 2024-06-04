import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.db_setup import Base, get_db
from db.models import *  # noqa
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


def test_user(client):
    response = client.post(
        "/auth/register",
        json={"username": "test_user", "password": "testpass"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert "access_token" in data
    client.token = data["access_token"]

    response = client.get("/users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "test_user"

    response = client.post(
        "/users/update",
        headers={"Authorization": f"Bearer {client.token}"},
        json={"username": "test_user", "email": "a@b.com"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "a@b.com"


def test_workspace(client):
    test_user(client)

    response = client.post(
        "/workspaces/create",
        headers={"Authorization": f"Bearer {client.token}"},
        json={"user_id": 1, "name": "test_workspace"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user_id"] == 1
    assert data["name"] == "test_workspace"
    client.ws_id = data["id"]


def test_user_workspace(client):
    test_workspace(client)

    response = client.get(
        f"/workspaces/{client.ws_id}/join",
        headers={"Authorization": f"Bearer {client.token}"},
    )
    assert response.status_code == 200, response.text


def test_room_user(client):
    test_user_workspace(client)

    response = client.post(
        "/room",
        headers={"Authorization": f"Bearer {client.token}"},
        json={"workspace_id": client.ws_id, "title": "test_room"},
    )
    assert response.status_code == 201, response.text
    client.room_id = response.json()["id"]

    response = client.get(
        f"/rooms/{client.room_id}/join",
        headers={"Authorization": f"Bearer {client.token}"},
    )
    assert response.status_code == 200, response.text
