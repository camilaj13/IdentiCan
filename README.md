# IdentiCan

Canine biometric identification platform using nose-print recognition. Register your dog, track vaccines, generate a unique QR code, and verify identity through AI-powered nose biometrics -- from your phone or computer.

## Mobile App

![IdentiCan Mobile App UI](docs/screenshots/identican_ui_overview.png)

## Web App

![IdentiCan Web Application](docs/screenshots/identican_webapp_overview.png)

## Architecture

![IdentiCan System Architecture](docs/screenshots/architecture_diagram.png)

Both the **mobile app** and the **web app** connect to the same backend and share the same database. A user (regular, admin, or verificador) can log in from either platform and see identical data.

```
Mobile App (React Native)  ──┐
                              ├──> FastAPI Backend ──> PostgreSQL
Web App (SPA at /app)      ──┘         │
                                       ├──> Pet-ReID-IMAG (ML)
Admin Dashboard (/admin)   ────────────┘
```

---

## Features

| Feature | Mobile | Web | Admin |
|---------|--------|-----|-------|
| Login / Register | Yes | Yes | Yes |
| My Dogs (list, add, edit, delete) | Yes | Yes | - |
| Dog Profile with details | Yes | Yes | View only |
| Vaccine Records (CRUD) | Yes | Yes | - |
| QR Code (generate, share, PDF) | Yes | Yes | - |
| Nose Biometric Verification | Yes | Yes | - |
| QR Code Verification | Yes | Yes | - |
| Multilanguage (ES / EN / PT) | Yes | Yes | EN |
| Admin Dashboard & Stats | - | - | Yes |
| Toggle Premium for users | - | - | Yes |

### Roles & Permissions

| Role | Description | Verification Limit |
|------|-------------|--------------------|
| **user** (Free) | Regular user | 3 per day |
| **user** (Premium) | Premium user | Unlimited |
| **admin** | Full platform access | Unlimited |
| **verificador** | Verifier role | 3 per day |

### ML Model

The biometric engine uses **Pet-ReID-IMAG** (3rd place, CVPR2022 Biometrics Workshop):
- **Backbone**: ResNeSt-101
- **Embeddings**: 2048-dimensional feature vectors
- **Matching**: Cosine similarity (configurable threshold, default 0.5)
- **Accuracy**: 91.7% on the pet identification benchmark

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI 0.109, SQLAlchemy 2.0, PostgreSQL |
| **Auth** | JWT (python-jose), bcrypt (passlib) |
| **Mobile App** | React Native 0.73, Expo SDK 50, React Native Paper |
| **Web App** | Vanilla JS SPA, served by FastAPI at `/app` |
| **Admin Dashboard** | Vanilla JS, served at `/admin` |
| **ML Model** | PyTorch, Pet-ReID-IMAG (ResNeSt-101) |
| **Storage** | Cloudflare R2 (S3-compatible) |
| **Rate Limiting** | slowapi (100 req/min) |
| **i18n** | 3 languages: Spanish, English, Portuguese |
| **Deployment** | Railway (backend), EAS (mobile) |

---

## Project Structure

```
IdentiCan/
├── backend/                 # FastAPI REST API
│   ├── app/
│   │   ├── api/             # Route handlers (auth, dogs, nose, vaccines, qr, admin)
│   │   ├── core/            # Config, database, security
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic validation schemas
│   │   └── utils/           # ML engine, storage, QR generator
│   ├── tests/               # pytest test suite (38 tests)
│   ├── requirements.txt
│   └── Dockerfile
├── mobile/                  # React Native + Expo mobile app
│   ├── src/
│   │   ├── screens/         # All app screens (Auth, MiCan, Verificador)
│   │   ├── components/      # Reusable components (DogCard, VaccineCard, etc.)
│   │   ├── context/         # AuthContext (JWT management)
│   │   ├── i18n/            # Translations (es, en, pt)
│   │   ├── api/             # Axios HTTP client
│   │   ├── navigation/      # React Navigation stacks + tabs
│   │   └── constants/       # Colors, config
│   └── package.json
├── webapp/                  # Web applications
│   ├── app.html             # User-facing web app (mirrors mobile)
│   ├── index.html           # Admin dashboard
│   └── static/
│       ├── webapp.js         # Web app SPA logic
│       ├── webapp.css        # Web app styles
│       ├── app.js            # Admin dashboard logic
│       └── styles.css        # Admin dashboard styles
├── ml_model/                # Pet-ReID-IMAG model
│   ├── fastreid/            # Model architecture
│   ├── configs/             # Training configs
│   └── logs/                # Trained weights
├── docs/                    # Documentation & screenshots
└── .github/                 # CI/CD workflows
```

---

## Setup Guide

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend API |
| PostgreSQL | 14+ | Database |
| Node.js | 18+ | Mobile app |
| npm | 9+ | Mobile dependencies |
| Expo Go | Latest | Run mobile app on phone |

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/camilaj13/IdentiCan.git
cd IdentiCan
```

---

### Step 2: Set Up the Backend

#### 2.1 Create a Python virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

#### 2.2 Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 2.3 Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set your values:

```env
# Required - change these
SECRET_KEY=your-random-secret-key-here
JWT_SECRET=your-random-jwt-secret-here
DATABASE_URL=postgresql://user:password@localhost:5432/identican

# Optional - adjust as needed
DEBUG=True
VERIFICATION_LIMIT_FREE=3
MATCH_THRESHOLD=0.5
CORS_ORIGINS=http://localhost:3000,http://localhost:19006
```

> **Tip**: Generate secure keys with `python -c "import secrets; print(secrets.token_hex(32))"`

#### 2.4 Create the PostgreSQL database

```bash
createdb identican
```

Tables are created automatically when the backend starts.

#### 2.5 (Optional) Download ML model weights

```bash
cd ../ml_model
python download_weights.py
cd ../backend
```

If weights are not available, the backend falls back to an ImageNet-pretrained backbone.

#### 2.6 Start the backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify it's running:
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

---

### Step 3: Set Up the Web App

The web app requires **no separate setup**. It is served directly by the FastAPI backend as static files.

Once the backend is running:

| App | URL | Who can use it |
|-----|-----|----------------|
| **Web App** | [http://localhost:8000/app](http://localhost:8000/app) | All users (user, admin, verificador) |
| **Admin Dashboard** | [http://localhost:8000/admin](http://localhost:8000/admin) | Admin users only |

The web app mirrors the mobile app exactly: same screens, same API endpoints, same database. Any account created on mobile works on the web, and vice versa.

---

### Step 4: Set Up the Mobile App

#### 4.1 Install Node.js dependencies

```bash
cd mobile
npm install
```

#### 4.2 Configure the API URL

Edit `src/constants/config.js` if your backend runs at a different address:

```javascript
export const API_URL = __DEV__
  ? 'http://localhost:8000'         // Development
  : 'https://identican.railway.app'; // Production
```

> **Important**: If testing on a physical phone, replace `localhost` with your computer's local IP address (e.g., `http://192.168.1.100:8000`).

#### 4.3 Start the mobile app

```bash
npx expo start
```

Then:
- **Physical phone**: Scan the QR code with the Expo Go app
- **Android emulator**: Press `a`
- **iOS simulator**: Press `i`

---

### Step 5: Create Your First Account

You can register from either the mobile app or the web app:

1. Open the app (mobile or web)
2. Tap **"Don't have an account? Sign up"**
3. Fill in: name, email, password (min 6 characters), phone (optional)
4. Tap **"Create Account"**

You are now logged in and can:
- Add dogs with full details
- Record vaccine history
- Generate QR codes for collars
- Verify dogs by nose scan or QR code

#### Creating an Admin user

There is no self-service admin registration. To make a user an admin, update the database directly:

```sql
UPDATE users SET role = 'admin' WHERE email = 'your-email@example.com';
```

---

## Running with Docker

### Backend only

```bash
cd backend
docker build -t identican-backend .
docker run -p 8000:8000 --env-file .env identican-backend
```

The web app and admin dashboard are included automatically (served from `/app` and `/admin`).

---

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

The test suite includes 38 tests covering:
- Authentication (register, login, JWT validation)
- Dog CRUD operations
- Vaccine management
- Nose biometric upload and verification
- ML engine (embedding extraction, cosine similarity, matching)
- End-to-end workflow
- Multilingual error messages

---

## API Reference

Base URL: `http://localhost:8000`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | No | Register new user |
| POST | `/api/auth/login` | No | Log in, get JWT token |
| GET | `/api/auth/me` | Yes | Get current user |
| POST | `/api/dogs` | Yes | Create a dog |
| GET | `/api/dogs` | Yes | List user's dogs |
| GET | `/api/dogs/{id}` | Yes | Get dog details |
| PUT | `/api/dogs/{id}` | Yes | Update dog |
| DELETE | `/api/dogs/{id}` | Yes | Delete dog |
| POST | `/api/vaccines` | Yes | Add vaccine record |
| GET | `/api/vaccines/dog/{id}` | Yes | List dog's vaccines |
| DELETE | `/api/vaccines/{id}` | Yes | Delete vaccine |
| POST | `/api/nose/upload` | Yes | Upload nose images (max 3) |
| POST | `/api/nose/verify` | Yes | Verify dog by nose scan |
| GET | `/api/qr/generate/{id}` | Yes | Get QR code as PNG |
| GET | `/api/qr/pdf/{id}` | Yes | Get QR code as PDF |
| GET | `/api/admin/stats` | Admin | Platform statistics |
| GET | `/api/admin/users-detail` | Admin | All users with dogs |
| POST | `/api/admin/users/{id}/premium` | Admin | Toggle premium |

Full interactive docs at `/docs` (Swagger) or `/redoc` (ReDoc).

---

## Database Schema

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    users     │     │     dogs     │     │   vaccines   │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ id           │──┐  │ id           │──┐  │ id           │
│ email        │  │  │ owner_id  ───│──┘  │ dog_id    ───│──┘
│ password_hash│  │  │ name         │     │ vaccine_type │
│ name         │  │  │ breed        │     │ vaccine_date │
│ phone        │  │  │ sex          │     │ next_dose    │
│ role         │  │  │ origin       │     │ vet_name     │
│ is_premium   │  │  │ age_years    │     │ clinic_name  │
│ created_at   │  │  │ weight_kg    │     │ batch_number │
│ updated_at   │  │  │ color        │     │ notes        │
└──────────────┘  │  │ nose_images  │     │ created_at   │
                  │  │ nose_embedding│     └──────────────┘
┌──────────────┐  │  │ qr_code      │
│verification_ │  │  │ microchip_id │
│    logs      │  │  │ behavior_notes│
├──────────────┤  │  │ likes        │
│ id           │  │  │ allergies    │
│ user_id   ───│──┘  │ created_at   │
│ dog_id       │     │ updated_at   │
│ type         │     └──────────────┘
│ success      │
│ confidence   │
│ date         │
│ created_at   │
└──────────────┘
```

---

## Documentation

- [Setup Guide](docs/SETUP.md)
- [API Reference](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Deployment](docs/DEPLOYMENT.md)

---

## License

Application code: MIT License. See [LICENSE.md](LICENSE.md).

The ML model (Pet-ReID-IMAG) retains its original license.
