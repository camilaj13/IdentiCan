"""Tests for nose biometric upload and verification endpoints."""

import io

from PIL import Image

from tests.conftest import client

DOG_DATA = {
    "name": "Luna",
    "breed": "Golden Retriever",
    "sex": "F",
    "origin": "adopted",
    "age_years": 2,
    "weight_kg": 28.0,
    "color": "dorado",
}


def _make_test_image(color: tuple = (128, 64, 32), size: tuple = (256, 256)) -> bytes:
    """Create a small in-memory JPEG image."""
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()


def _register_and_get_token(email: str = "nose_user@example.com") -> str:
    resp = client.post(
        "/api/auth/register",
        json={"email": email, "password": "password123", "name": "Test User"},
    )
    return resp.json()["access_token"]


def _create_dog(token: str) -> int:
    resp = client.post(
        "/api/dogs",
        json=DOG_DATA,
        headers={"Authorization": f"Bearer {token}"},
    )
    return resp.json()["id"]


class TestNoseUpload:
    def test_upload_single_image(self):
        token = _register_and_get_token("upload1@example.com")
        dog_id = _create_dog(token)
        img = _make_test_image()

        resp = client.post(
            f"/api/nose/upload?dog_id={dog_id}",
            files=[("files", ("nose.jpg", img, "image/jpeg"))],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["dog_id"] == dog_id
        assert len(data["nose_images"]) == 1
        assert data["embedding_computed"] is True
        assert data["embedding_dim"] == 2048

    def test_upload_multiple_images(self):
        token = _register_and_get_token("upload2@example.com")
        dog_id = _create_dog(token)

        files = [
            ("files", ("nose1.jpg", _make_test_image((100, 50, 25)), "image/jpeg")),
            ("files", ("nose2.jpg", _make_test_image((120, 60, 30)), "image/jpeg")),
            ("files", ("nose3.jpg", _make_test_image((140, 70, 35)), "image/jpeg")),
        ]
        resp = client.post(
            f"/api/nose/upload?dog_id={dog_id}",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["nose_images"]) == 3
        assert data["embedding_computed"] is True
        assert data["embedding_dim"] == 2048

    def test_upload_too_many_images(self):
        token = _register_and_get_token("upload3@example.com")
        dog_id = _create_dog(token)

        files = [
            ("files", (f"nose{i}.jpg", _make_test_image(), "image/jpeg"))
            for i in range(4)
        ]
        resp = client.post(
            f"/api/nose/upload?dog_id={dog_id}",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 400

    def test_upload_not_image(self):
        token = _register_and_get_token("upload4@example.com")
        dog_id = _create_dog(token)

        resp = client.post(
            f"/api/nose/upload?dog_id={dog_id}",
            files=[("files", ("data.txt", b"not an image", "text/plain"))],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 400

    def test_upload_wrong_dog(self):
        token = _register_and_get_token("upload5@example.com")
        img = _make_test_image()

        resp = client.post(
            "/api/nose/upload?dog_id=99999",
            files=[("files", ("nose.jpg", img, "image/jpeg"))],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 404


class TestNoseVerify:
    def test_verify_matches_registered_dog(self):
        """Upload a nose image, then verify with the same image — should match."""
        token = _register_and_get_token("verify1@example.com")
        dog_id = _create_dog(token)
        nose_img = _make_test_image(color=(80, 40, 20))

        # Upload nose
        client.post(
            f"/api/nose/upload?dog_id={dog_id}",
            files=[("files", ("nose.jpg", nose_img, "image/jpeg"))],
            headers={"Authorization": f"Bearer {token}"},
        )

        # Verify with the same image
        resp = client.post(
            "/api/nose/verify",
            files=[("file", ("scan.jpg", nose_img, "image/jpeg"))],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["match"] is True
        assert data["dog_id"] == dog_id
        assert data["confidence"] > 0.5

    def test_verify_no_dogs_registered(self):
        """Verify when no dogs have embeddings — should not match."""
        token = _register_and_get_token("verify2@example.com")
        nose_img = _make_test_image()

        resp = client.post(
            "/api/nose/verify",
            files=[("file", ("scan.jpg", nose_img, "image/jpeg"))],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["match"] is False
        assert data["dog_id"] is None

    def test_verify_not_image(self):
        token = _register_and_get_token("verify3@example.com")
        resp = client.post(
            "/api/nose/verify",
            files=[("file", ("data.txt", b"not an image", "text/plain"))],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 400

    def test_verify_daily_limit(self):
        """Free users are limited to 3 verifications per day."""
        token = _register_and_get_token("verify4@example.com")
        # Create a dog with nose so verification logic runs fully
        dog_id = _create_dog(token)
        nose_img = _make_test_image()
        client.post(
            f"/api/nose/upload?dog_id={dog_id}",
            files=[("files", ("nose.jpg", nose_img, "image/jpeg"))],
            headers={"Authorization": f"Bearer {token}"},
        )

        for _ in range(3):
            resp = client.post(
                "/api/nose/verify",
                files=[("file", ("scan.jpg", nose_img, "image/jpeg"))],
                headers={"Authorization": f"Bearer {token}"},
            )
            assert resp.status_code == 200

        # 4th should be rate-limited
        resp = client.post(
            "/api/nose/verify",
            files=[("file", ("scan.jpg", nose_img, "image/jpeg"))],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 429


class TestMLEngine:
    """Unit tests for the ml_engine utilities."""

    def test_compute_similarity_identical(self):
        from app.utils.ml_engine import compute_similarity

        emb = [1.0, 2.0, 3.0, 4.0]
        assert compute_similarity(emb, emb) > 0.99

    def test_compute_similarity_orthogonal(self):
        from app.utils.ml_engine import compute_similarity

        a = [1.0, 0.0]
        b = [0.0, 1.0]
        assert abs(compute_similarity(a, b)) < 0.01

    def test_find_best_match_above_threshold(self):
        from app.utils.ml_engine import find_best_match

        query = [1.0, 0.0, 0.0]
        gallery = [
            (1, [0.0, 1.0, 0.0]),  # orthogonal
            (2, [0.9, 0.1, 0.0]),  # similar
        ]
        result = find_best_match(query, gallery, threshold=0.5)
        assert result is not None
        assert result[0] == 2
        assert result[1] > 0.5

    def test_find_best_match_below_threshold(self):
        from app.utils.ml_engine import find_best_match

        query = [1.0, 0.0, 0.0]
        gallery = [
            (1, [0.0, 1.0, 0.0]),
            (2, [0.0, 0.0, 1.0]),
        ]
        result = find_best_match(query, gallery, threshold=0.9)
        assert result is None

    def test_find_best_match_empty_gallery(self):
        from app.utils.ml_engine import find_best_match

        result = find_best_match([1.0, 2.0], [], threshold=0.5)
        assert result is None

    def test_extract_embedding_returns_2048(self):
        from app.utils.ml_engine import extract_embedding

        img_bytes = _make_test_image()
        emb = extract_embedding(img_bytes)
        assert isinstance(emb, list)
        assert len(emb) == 2048

    def test_extract_embedding_multi_returns_2048(self):
        from app.utils.ml_engine import extract_embedding_multi

        imgs = [_make_test_image((100, 50, 25)), _make_test_image((120, 60, 30))]
        emb = extract_embedding_multi(imgs)
        assert isinstance(emb, list)
        assert len(emb) == 2048

    def test_same_image_produces_same_embedding(self):
        from app.utils.ml_engine import compute_similarity, extract_embedding

        img = _make_test_image()
        emb1 = extract_embedding(img)
        emb2 = extract_embedding(img)
        assert compute_similarity(emb1, emb2) > 0.99
