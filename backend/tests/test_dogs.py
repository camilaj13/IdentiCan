"""Tests for dog CRUD endpoints."""

from tests.conftest import client

DOG_DATA = {
    "name": "Firulais",
    "breed": "Labrador",
    "sex": "M",
    "origin": "adopted",
    "age_years": 3,
    "weight_kg": 25.5,
    "color": "dorado",
}


def _register_and_get_token(email: str = "dogowner@example.com") -> str:
    """Register a user and return the auth token."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "password123",
            "name": "Dog Owner",
        },
    )
    return response.json()["access_token"]


class TestCreateDog:
    def test_create_dog_success(self):
        token = _register_and_get_token("create@example.com")
        response = client.post(
            "/api/dogs",
            json=DOG_DATA,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Firulais"
        assert data["breed"] == "Labrador"
        assert data["sex"] == "M"
        assert data["qr_code"].startswith("IDC-DOG-")
        assert data["owner_id"] is not None

    def test_create_dog_unauthenticated(self):
        response = client.post("/api/dogs", json=DOG_DATA)
        assert response.status_code == 401

    def test_create_dog_invalid_sex(self):
        token = _register_and_get_token("invalid_sex@example.com")
        bad_data = {**DOG_DATA, "sex": "X"}
        response = client.post(
            "/api/dogs",
            json=bad_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422


class TestListDogs:
    def test_list_dogs_empty(self):
        token = _register_and_get_token("empty_list@example.com")
        response = client.get(
            "/api/dogs", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_list_dogs_with_data(self):
        token = _register_and_get_token("with_data@example.com")
        client.post(
            "/api/dogs",
            json=DOG_DATA,
            headers={"Authorization": f"Bearer {token}"},
        )
        response = client.get(
            "/api/dogs", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        dogs = response.json()
        assert len(dogs) == 1
        assert dogs[0]["name"] == "Firulais"


class TestGetDog:
    def test_get_dog_success(self):
        token = _register_and_get_token("get_dog@example.com")
        create_resp = client.post(
            "/api/dogs",
            json=DOG_DATA,
            headers={"Authorization": f"Bearer {token}"},
        )
        dog_id = create_resp.json()["id"]

        response = client.get(
            f"/api/dogs/{dog_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == dog_id

    def test_get_dog_not_found(self):
        token = _register_and_get_token("not_found@example.com")
        response = client.get(
            "/api/dogs/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404


class TestUpdateDog:
    def test_update_dog_success(self):
        token = _register_and_get_token("update@example.com")
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
        # Unchanged fields should persist
        assert response.json()["breed"] == "Labrador"


class TestDeleteDog:
    def test_delete_dog_success(self):
        token = _register_and_get_token("delete@example.com")
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

        # Verify it's gone
        get_resp = client.get(
            f"/api/dogs/{dog_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert get_resp.status_code == 404

    def test_delete_nonexistent_dog(self):
        token = _register_and_get_token("delete_ne@example.com")
        response = client.delete(
            "/api/dogs/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
