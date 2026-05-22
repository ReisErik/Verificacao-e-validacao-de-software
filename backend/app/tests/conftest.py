import pytest
from sqlmodel import Session, create_engine, SQLModel
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import get_session
from app.models.user import User

DATABASE_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_TEST_URL, 
    connect_args={"check_same_thread": False}
    )

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session):
    with TestClient(app) as client:
        yield client