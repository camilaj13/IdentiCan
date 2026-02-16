# API Documentation - IdentiCan

Base URL: `http://localhost:8000`

Interactive documentation: `http://localhost:8000/docs`

---

## Authentication

All protected endpoints require the header:
```
Authorization: Bearer <token>
```

### POST /api/auth/register

Register a new user.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "mypassword123",
  "name": "John Smith",
  "phone": "+1234567890"
}
```

**Response (201):**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Smith",
    "role": "user",
    "is_premium": false
  }
}
```

### POST /api/auth/login

**Body:**
```json
{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

### GET /api/auth/me

Get authenticated user data. Requires token.

---

## Dogs

### POST /api/dogs

Register a new dog. Requires token.

**Body:**
```json
{
  "name": "Buddy",
  "breed": "Labrador",
  "sex": "M",
  "origin": "adopted",
  "age_years": 3,
  "weight_kg": 25.5,
  "color": "golden"
}
```

### GET /api/dogs

List user's dogs. Requires token.

### GET /api/dogs/{id}

Get a dog by ID. Requires token.

### PUT /api/dogs/{id}

Update a dog (owner only). Requires token.

### DELETE /api/dogs/{id}

Delete a dog (owner only). Requires token.

---

## Nose / Biometrics

### POST /api/nose/upload

Upload nose images for a dog.

**Form Data:**
- `dog_id`: Dog ID
- `files`: Up to 3 image files

### POST /api/nose/verify

Verify a dog by nose scan.

**Limit:** 3 verifications/day for free users.

**Form Data:**
- `file`: Nose image

**Response (200):**
```json
{
  "match": true,
  "confidence": 0.92,
  "dog_id": 1,
  "dog_name": "Buddy",
  "verification_usage": {
    "limit": 3,
    "used": 1,
    "remaining": 2
  }
}
```

**Response (429) - Limit reached:**
```json
{
  "error": "Daily limit reached",
  "verifications_used": 3,
  "verifications_limit": 3,
  "message": "Upgrade to Premium for unlimited verifications"
}
```

---

## Vaccines

### POST /api/vaccines

Add a vaccine. Requires token.

**Body:**
```json
{
  "dog_id": 1,
  "vaccine_type": "Rabies",
  "vaccine_date": "2024-01-15",
  "veterinarian_name": "Dr. Smith",
  "clinic_name": "Vet Center"
}
```

### GET /api/vaccines/dog/{dog_id}

List vaccines for a dog. Requires token.

### DELETE /api/vaccines/{id}

Delete a vaccine. Requires token.

---

## QR

### GET /api/qr/generate/{dog_id}

Generate QR as PNG. Requires token.

### GET /api/qr/pdf/{dog_id}

Generate QR as 3x3cm PDF. Requires token.

---

## Admin (role=admin)

### GET /api/admin/users

List all users.

### GET /api/admin/dogs

List all dogs.

### POST /api/admin/users/{id}/premium

Activate/deactivate Premium.

### GET /api/admin/stats

General statistics.

---

## Payments (Phase 2)

### GET /api/payments/plans

View available plans.

### POST /api/payments/checkout

Create payment session (placeholder).

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid data |
| 401 | Not authenticated |
| 403 | No permissions |
| 404 | Not found |
| 429 | Verification limit reached |
| 500 | Internal error |
