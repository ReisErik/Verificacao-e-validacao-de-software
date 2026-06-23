import pytest
from sqlmodel import Session, create_engine, SQLModel
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import get_session
from app.models.user import User
from app.core.auth import get_current_user
from datetime import datetime, UTC

DATABASE_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_TEST_URL,
    connect_args={"check_same_thread": False}
)

def override_get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def create_user(
    *,
    id=None,
    first_name="Test",
    last_name="User",
    unique_name="testuser",
    email="test@example.com",
    password="hashed_password",
    role="user",
    active=True,
    xp=0,
):
    return User(
        id=id,
        first_name=first_name,
        last_name=last_name,
        unique_name=unique_name,
        email=email,
        password=password,
        xp=xp,
        streak=0,
        best_streak=0,
        role=role,
        active=active,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

def override_get_current_user(user):
    def _get_user():
        return user
    return _get_user

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def users(session):
    user1 = create_user(
        id=1,
        email="user1@test.com",
        unique_name="user1"
    )

    user2 = create_user(
        id=2,
        email="user2@test.com",
        unique_name="user2"
    )

    session.add(user1)
    session.add(user2)
    session.commit()

    return {"user1": user1, "user2": user2}

@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client