# Documentación de la API - IdentiCan

Base URL: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

---

## Autenticación

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer <token>
```

### POST /api/auth/register

Registrar un nuevo usuario.

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "mipassword123",
  "name": "Juan Pérez",
  "phone": "+5491112345678"
}
```

**Response (201):**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "name": "Juan Pérez",
    "role": "user",
    "is_premium": false
  }
}
```

### POST /api/auth/login

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "mipassword123"
}
```

### GET /api/auth/me

Obtener datos del usuario autenticado. Requiere token.

---

## Perros

### POST /api/dogs

Registrar un nuevo perro. Requiere token.

**Body:**
```json
{
  "name": "Firulais",
  "breed": "Labrador",
  "sex": "M",
  "origin": "adopted",
  "age_years": 3,
  "weight_kg": 25.5,
  "color": "dorado"
}
```

### GET /api/dogs

Listar perros del usuario. Requiere token.

### GET /api/dogs/{id}

Obtener un perro por ID. Requiere token.

### PUT /api/dogs/{id}

Actualizar un perro (solo dueño). Requiere token.

### DELETE /api/dogs/{id}

Eliminar un perro (solo dueño). Requiere token.

---

## Nariz / Biometría

### POST /api/nose/upload

Subir imágenes de la nariz de un perro.

**Form Data:**
- `dog_id`: ID del perro
- `files`: Hasta 3 archivos de imagen

### POST /api/nose/verify

Verificar un perro por escaneo de nariz.

**Límite:** 3 verificaciones/día para usuarios gratuitos.

**Form Data:**
- `file`: Imagen de la nariz

**Response (200):**
```json
{
  "match": true,
  "confidence": 0.92,
  "dog_id": 1,
  "dog_name": "Firulais",
  "verification_usage": {
    "limit": 3,
    "used": 1,
    "remaining": 2
  }
}
```

**Response (429) - Límite alcanzado:**
```json
{
  "error": "Límite diario alcanzado",
  "verifications_used": 3,
  "verifications_limit": 3,
  "message": "Upgrade a Premium para verificaciones ilimitadas"
}
```

---

## Vacunas

### POST /api/vaccines

Agregar una vacuna. Requiere token.

**Body:**
```json
{
  "dog_id": 1,
  "vaccine_type": "Antirrábica",
  "vaccine_date": "2024-01-15",
  "veterinarian_name": "Dr. García",
  "clinic_name": "Vet Center"
}
```

### GET /api/vaccines/dog/{dog_id}

Listar vacunas de un perro. Requiere token.

### DELETE /api/vaccines/{id}

Eliminar una vacuna. Requiere token.

---

## QR

### GET /api/qr/generate/{dog_id}

Generar QR en formato PNG. Requiere token.

### GET /api/qr/pdf/{dog_id}

Generar QR en formato PDF 3x3cm. Requiere token.

---

## Admin (role=admin)

### GET /api/admin/users

Listar todos los usuarios.

### GET /api/admin/dogs

Listar todos los perros.

### POST /api/admin/users/{id}/premium

Activar/desactivar Premium.

### GET /api/admin/stats

Estadísticas generales.

---

## Pagos (Fase 2)

### GET /api/payments/plans

Ver planes disponibles.

### POST /api/payments/checkout

Crear sesión de pago (placeholder).

---

## Códigos de Error

| Código | Significado |
|--------|-------------|
| 400 | Datos inválidos |
| 401 | No autenticado |
| 403 | Sin permisos |
| 404 | No encontrado |
| 429 | Límite de verificaciones alcanzado |
| 500 | Error interno |
