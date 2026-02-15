"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

# In-memory SQLite for tests
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


class TestRegister:
    def test_register_success(self):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["name"] == "Test User"

    def test_register_duplicate_email(self):
        client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password123",
                "name": "First User",
            },
        )
        response = client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password456",
                "name": "Second User",
            },
        )
        assert response.status_code == 400

    def test_register_short_password(self):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "short@example.com",
                "password": "12345",
                "name": "Short Pass",
            },
        )
        assert response.status_code == 400


class TestLogin:
    def test_login_success(self):
        # Register first
        client.post(
            "/api/auth/register",
            json={
                "email": "login@example.com",
                "password": "password123",
                "name": "Login User",
            },
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_password(self):
        response = client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "wrongpass"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self):
        response = client.post(
            "/api/auth/login",
            json={"email": "nobody@example.com", "password": "password123"},
        )
        assert response.status_code == 401


class TestMe:
    def test_get_me_authenticated(self):
        # Register and get token
        reg = client.post(
            "/api/auth/register",
            json={
                "email": "me@example.com",
                "password": "password123",
                "name": "Me User",
            },
        )
        token = reg.json()["access_token"]

        response = client.get(
            "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == "me@example.com"

    def test_get_me_unauthenticated(self):
        response = client.get("/api/auth/me")
        assert response.status_code == 401
