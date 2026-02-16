# Deployment Guide - IdentiCan

## Backend - Railway

### 1. Create project on Railway

1. Go to [railway.app](https://railway.app)
2. Create a new project
3. Connect with the GitHub repository

### 2. Configure database

1. Add a PostgreSQL service
2. Copy the generated `DATABASE_URL`

### 3. Environment variables

Configure on Railway:

```
APP_NAME=IdentiCan
DEBUG=False
SECRET_KEY=<generate-secure-key>
DATABASE_URL=<railway-postgres-url>
JWT_SECRET=<generate-secure-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=https://identican.app
VERIFICATION_LIMIT_FREE=3
```

### 4. Deploy

Railway automatically detects the Dockerfile and deploys.

The healthcheck is configured at `/health`.

---

## Mobile - Expo / EAS

### 1. Configure Expo

```bash
cd mobile
npx expo login
```

### 2. Configure EAS Build

```bash
npx eas-cli build:configure
```

### 3. Build for Android

```bash
eas build --platform android
```

### 4. Build for iOS

```bash
eas build --platform ios
```

### 5. Publish OTA updates

```bash
eas update --branch production
```

---

## CI/CD with GitHub Actions

Workflows are configured in `.github/workflows/`:

- **backend-deploy.yml**: Tests + deploy to Railway on push to main
- **mobile-build.yml**: Lint + build with EAS on push to main

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `RAILWAY_TOKEN` | Railway API token |
| `EXPO_TOKEN` | Expo / EAS token |

---

## Monitoring

- Railway dashboard for backend logs
- Expo dashboard for mobile builds and analytics
- `/health` endpoint for health checks
