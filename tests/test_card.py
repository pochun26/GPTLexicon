from fastapi.testclient import TestClient
from app.main import app
from app.cards.models import Base
from app.dependencies import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_root():
    response = client.get("/cards")
    assert response.status_code == 200


def test_create():
    response = client.get("/card/test")
    assert response.status_code == 404
    response = client.post("/card", json={"word": "test"})
    assert response.status_code == 200
    response = client.get("/card/test")
    assert response.status_code == 200


def test_delete():
    client.post("/card", json={"word": "test"})
    response = client.delete("/card/test")
    assert response.status_code == 200
    response = client.get("/card/test")
    assert response.status_code == 404
