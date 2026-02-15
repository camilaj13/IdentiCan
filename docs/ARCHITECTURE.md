# Arquitectura - IdentiCan

## Visión General

IdentiCan es una plataforma de identificación biométrica canina compuesta por:

1. **Backend API** (FastAPI + PostgreSQL)
2. **App Móvil** (React Native + Expo)
3. **Modelo ML** (Pet-ReID-IMAG, para identificación por nariz)

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────┐
│   App Móvil     │────▸│   Backend API    │────▸│  PostgreSQL  │
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

### Estructura

```
backend/app/
├── api/          # Endpoints REST
├── core/         # Config, DB, Security
├── models/       # SQLAlchemy ORM
├── schemas/      # Pydantic validation
└── utils/        # QR, Storage helpers
```

### Flujo de Autenticación

1. Usuario se registra/login → recibe JWT
2. Cada request envía `Authorization: Bearer <token>`
3. Middleware valida el token y extrae el usuario
4. Decoradores de rol verifican permisos

### Modelos de Datos

- **User**: Datos del usuario, rol, estado premium
- **Dog**: Datos del perro, imágenes de nariz, QR, embedding
- **Vaccine**: Registro de vacunas por perro
- **VerificationLog**: Log de verificaciones para control de límites

### Límite de Verificaciones

Los usuarios gratuitos tienen 3 verificaciones por día.
Se cuenta por `VerificationLog` con `date = today()`.
Usuarios premium y admin no tienen límite.

## Mobile

### Navegación

```
App
├── AuthNavigator (sin token)
│   ├── LoginScreen
│   └── RegisterScreen
└── MainTabs (con token)
    ├── MiCan (Tab)
    │   ├── HomeScreen
    │   ├── AddDogScreen
    │   ├── DogProfileScreen
    │   ├── VaccinesScreen
    │   └── GenerateQRScreen
    └── Verificador (Tab)
        ├── ScanNoseScreen
        ├── ScanQRScreen
        └── ResultScreen
```

### Estado Global

- **AuthContext**: Token JWT, datos del usuario, login/logout
- Las pantallas manejan su estado local con hooks

## Modelo ML

El directorio `ml_model/` contiene el modelo Pet-ReID-IMAG:
- Backbone: ResNeSt
- Entrenado en escalas 224, 256, 288
- Precisión: 91.7% (Phase A), 86.27% (Phase B)

La integración con el backend se hará en una fase futura.
Actualmente, la verificación de nariz retorna resultados mock.

## Seguridad

- Passwords hasheados con bcrypt (rounds=12)
- JWT con HS256, expiración 7 días
- Rate limiting: 100 req/min
- CORS configurado por origins
- ORM previene SQL injection
- Secrets solo desde variables de entorno
