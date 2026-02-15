"""Tests for dog CRUD endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def _get_auth_token(email: str = "dogowner@example.com") -> str:
    """Helper: register a user and return the auth token."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "password123",
            "name": "Dog Owner",
        },
    )
    if response.status_code == 400:
        # Already registered, login instead
        response = client.post(
            "/api/auth/login",
            json={"email": email, "password": "password123"},
        )
    return response.json()["access_token"]


DOG_DATA = {
    "name": "Firulais",
    "breed": "Labrador",
    "sex": "M",
    "origin": "adopted",
    "age_years": 3,
    "weight_kg": 25.5,
    "color": "dorado",
}


class TestCreateDog:
    def test_create_dog_success(self):
        token = _get_auth_token("create_dog@example.com")
        response = client.post(
            "/api/dogs",
            json=DOG_DATA,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Firulais"
        assert data["qr_code"].startswith("IDC-DOG-")

    def test_create_dog_unauthenticated(self):
        response = client.post("/api/dogs", json=DOG_DATA)
        assert response.status_code == 401


class TestListDogs:
    def test_list_dogs(self):
        token = _get_auth_token("list_dogs@example.com")
        # Create a dog first
        client.post(
            "/api/dogs",
            json=DOG_DATA,
            headers={"Authorization": f"Bearer {token}"},
        )
        response = client.get(
            "/api/dogs", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1


class TestUpdateDog:
    def test_update_dog(self):
        token = _get_auth_token("update_dog@example.com")
        create_resp = client.post(
            "/api/dogs",
            json=DOG_DATA,
            headers={"Authorization": f"Bearer {token}"},
        )
        dog_id = create_resp.json()["id"]

        response = client.put(
            f"/api/dogs/{dog_id}",
            json={"name": "Firulais Jr.", "weight_kg": 28.0},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Firulais Jr."
        assert response.json()["weight_kg"] == 28.0


class TestDeleteDog:
    def test_delete_dog(self):
        token = _get_auth_token("delete_dog@example.com")
        create_resp = client.post(
            "/api/dogs",
            json=DOG_DATA,
            headers={"Authorization": f"Bearer {token}"},
        )
        dog_id = create_resp.json()["id"]

        response = client.delete(
            f"/api/dogs/{dog_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204

    def test_delete_nonexistent_dog(self):
        token = _get_auth_token("delete_dog2@example.com")
        response = client.delete(
            "/api/dogs/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
