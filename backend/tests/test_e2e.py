"""End-to-end integration tests covering the full user workflow.

Tests the complete flow: register -> create dog -> upload nose -> verify -> vaccines -> QR.
"""

import io

from PIL import Image

from tests.conftest import client


def _make_nose_image(color: tuple = (128, 64, 32), size: tuple = (256, 256)) -> bytes:
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()


class TestFullWorkflow:
    """Tests the complete IdentiCan user workflow end-to-end."""

    def test_complete_workflow(self):
        # 1. Register
        resp = client.post(
            "/api/auth/register",
            json={"email": "e2e@test.com", "password": "password123", "name": "E2E User"},
        )
        assert resp.status_code == 201
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Verify user profile
        resp = client.get("/api/auth/me", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "e2e@test.com"

        # 3. Create a dog
        resp = client.post(
            "/api/dogs",
            json={
                "name": "Buddy",
                "breed": "Beagle",
                "sex": "M",
                "origin": "adopted",
                "age_years": 4,
                "weight_kg": 12.0,
                "color": "tricolor",
            },
            headers=headers,
        )
        assert resp.status_code == 201
        dog = resp.json()
        dog_id = dog["id"]
        assert dog["name"] == "Buddy"
        assert dog["qr_code"].startswith("IDC-DOG-")

        # 4. Upload nose images
        nose_img = _make_nose_image()
        resp = client.post(
            f"/api/nose/upload?dog_id={dog_id}",
            files=[("files", ("nose.jpg", nose_img, "image/jpeg"))],
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["embedding_computed"] is True
        assert resp.json()["embedding_dim"] == 2048

        # 5. Verify nose matches
        resp = client.post(
            "/api/nose/verify",
            files=[("file", ("scan.jpg", nose_img, "image/jpeg"))],
            headers=headers,
        )
        assert resp.status_code == 200
        verify = resp.json()
        assert verify["match"] is True
        assert verify["dog_id"] == dog_id
        assert verify["confidence"] > 0.9

        # 6. Add a vaccine
        resp = client.post(
            "/api/vaccines",
            json={
                "dog_id": dog_id,
                "vaccine_type": "Rabies",
                "vaccine_date": "2025-06-01",
                "veterinarian_name": "Dr. Smith",
                "clinic_name": "VetClinic",
            },
            headers=headers,
        )
        assert resp.status_code == 201
        assert resp.json()["vaccine_type"] == "Rabies"

        # 7. List vaccines
        resp = client.get(f"/api/vaccines/dog/{dog_id}", headers=headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        # 8. Generate QR code PNG
        resp = client.get(f"/api/qr/generate/{dog_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "image/png"

        # 9. Generate QR code PDF
        resp = client.get(f"/api/qr/pdf/{dog_id}", headers=headers)
        assert resp.status_code == 200
        assert "pdf" in resp.headers["content-type"]

        # 10. List dogs
        resp = client.get("/api/dogs", headers=headers)
        assert resp.status_code == 200
        dogs = resp.json()
        assert len(dogs) == 1
        assert dogs[0]["name"] == "Buddy"

    def test_multilingual_errors(self):
        """Verify error messages in different languages."""
        resp = client.post(
            "/api/auth/register",
            json={"email": "lang@test.com", "password": "password123", "name": "Lang User"},
        )
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # English (default)
        resp = client.get("/api/dogs/99999", headers=headers)
        assert resp.status_code == 404

        # Spanish
        resp = client.get(
            "/api/dogs/99999", headers={**headers, "Accept-Language": "es"}
        )
        assert resp.status_code == 404
        assert "no encontrado" in resp.json()["detail"].lower()

        # Portuguese
        resp = client.get(
            "/api/dogs/99999", headers={**headers, "Accept-Language": "pt"}
        )
        assert resp.status_code == 404
        assert "não encontrado" in resp.json()["detail"].lower()
