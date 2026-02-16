"""Tests for authentication endpoints."""

from tests.conftest import client


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
        assert data["user"]["role"] == "user"
        assert data["user"]["is_premium"] is False

    def test_register_duplicate_email(self):
        client.post(
            "/api/auth/register",
            json={
                "email": "dup@example.com",
                "password": "password123",
                "name": "First User",
            },
        )
        response = client.post(
            "/api/auth/register",
            json={
                "email": "dup@example.com",
                "password": "password456",
                "name": "Second User",
            },
        )
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()

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
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        client.post(
            "/api/auth/register",
            json={
                "email": "wrong@example.com",
                "password": "password123",
                "name": "Wrong Pass",
            },
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "wrong@example.com", "password": "badpassword"},
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
        assert response.json()["name"] == "Me User"

    def test_get_me_unauthenticated(self):
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self):
        response = client.get(
            "/api/auth/me", headers={"Authorization": "Bearer invalidtoken123"}
        )
        assert response.status_code == 401
