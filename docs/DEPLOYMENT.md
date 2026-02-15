# Guía de Deployment - IdentiCan

## Backend - Railway

### 1. Crear proyecto en Railway

1. Ir a [railway.app](https://railway.app)
2. Crear nuevo proyecto
3. Conectar con el repositorio de GitHub

### 2. Configurar base de datos

1. Agregar servicio PostgreSQL
2. Copiar la `DATABASE_URL` generada

### 3. Variables de entorno

Configurar en Railway:

```
APP_NAME=IdentiCan
DEBUG=False
SECRET_KEY=<generar-clave-segura>
DATABASE_URL=<url-de-railway-postgres>
JWT_SECRET=<generar-clave-segura>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=https://identican.app
VERIFICATION_LIMIT_FREE=3
```

### 4. Deploy

Railway detecta automáticamente el Dockerfile y despliega.

El healthcheck está configurado en `/health`.

---

## Mobile - Expo / EAS

### 1. Configurar Expo

```bash
cd mobile
npx expo login
```

### 2. Configurar EAS Build

```bash
npx eas-cli build:configure
```

### 3. Build para Android

```bash
eas build --platform android
```

### 4. Build para iOS

```bash
eas build --platform ios
```

### 5. Publicar actualizaciones OTA

```bash
eas update --branch production
```

---

## CI/CD con GitHub Actions

Los workflows están configurados en `.github/workflows/`:

- **backend-deploy.yml**: Tests + deploy a Railway en push a main
- **mobile-build.yml**: Lint + build con EAS en push a main

### Secrets necesarios en GitHub

| Secret | Descripción |
|--------|-------------|
| `RAILWAY_TOKEN` | Token de API de Railway |
| `EXPO_TOKEN` | Token de Expo / EAS |

---

## Monitoreo

- Railway dashboard para logs del backend
- Expo dashboard para builds y analytics mobile
- `/health` endpoint para health checks
