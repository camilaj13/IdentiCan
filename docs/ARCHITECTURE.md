# Architecture - IdentiCan

## Overview

IdentiCan is a canine biometric identification platform composed of:

1. **Backend API** (FastAPI + PostgreSQL)
2. **Mobile App** (React Native + Expo)
3. **ML Model** (Pet-ReID-IMAG, for nose identification)

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────┐
│   Mobile App    │────▸│   Backend API    │────▸│  PostgreSQL  │
│  React Native   │     │    FastAPI       │     │              │
└─────────────────┘     └──────────────────┘     └──────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Cloudflare  │
                        │     R2       │
                        │  (Storage)   │
                        └──────────────┘
```

## Backend

### Structure

```
backend/app/
├── api/          # REST endpoints
├── core/         # Config, DB, Security
├── models/       # SQLAlchemy ORM
├── schemas/      # Pydantic validation
└── utils/        # QR, Storage helpers
```

### Authentication Flow

1. User registers/logs in → receives JWT
2. Each request sends `Authorization: Bearer <token>`
3. Middleware validates the token and extracts the user
4. Role decorators verify permissions

### Data Models

- **User**: User data, role, premium status
- **Dog**: Dog data, nose images, QR, embedding
- **Vaccine**: Vaccine records per dog
- **VerificationLog**: Verification log for limit tracking

### Verification Limit

Free users have 3 verifications per day.
Counted via `VerificationLog` with `date = today()`.
Premium and admin users have no limit.

## Mobile

### Navigation

```
App
├── AuthNavigator (no token)
│   ├── LoginScreen
│   └── RegisterScreen
└── MainTabs (with token)
    ├── My Dogs (Tab)
    │   ├── HomeScreen
    │   ├── AddDogScreen
    │   ├── DogProfileScreen
    │   ├── VaccinesScreen
    │   └── GenerateQRScreen
    └── Verifier (Tab)
        ├── ScanNoseScreen
        ├── ScanQRScreen
        └── ResultScreen
```

### Global State

- **AuthContext**: JWT token, user data, login/logout
- Screens manage their own local state with hooks

## ML Model

The `ml_model/` directory contains the Pet-ReID-IMAG model:
- Backbone: ResNeSt
- Trained at scales 224, 256, 288
- Accuracy: 91.7% (Phase A), 86.27% (Phase B)

Integration with the backend will be done in a future phase.
Currently, nose verification returns mock results.

## Security

- Passwords hashed with bcrypt (rounds=12)
- JWT with HS256, 7-day expiration
- Rate limiting: 100 req/min
- CORS configured by origins
- ORM prevents SQL injection
- Secrets loaded from environment variables only
