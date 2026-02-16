# IdentiCan

Canine biometric identification platform using nose photography. Register your dog, track vaccines, and generate a unique QR code for identification.

## App Preview

![IdentiCan Mobile App UI](docs/screenshots/identican_ui_overview.png)

## Features

- **Dog registration** with full details (breed, weight, origin, etc.)
- **Biometric identification** via nose print (based on Pet-ReID-IMAG)
- **Unique QR code** per dog (PNG + 3x3cm PDF for collar tag)
- **Vaccine records** with complete history
- **Roles**: user, verifier, admin
- **Multilanguage**: English, Spanish, Portuguese

## Project Structure

```
IdentiCan/
├── backend/       # REST API (FastAPI + PostgreSQL)
├── mobile/        # Mobile app (React Native + Expo)
├── ml_model/      # ML model (Pet-ReID-IMAG)
├── docs/          # Documentation
└── .github/       # CI/CD workflows
```

## Quick Start

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your values
uvicorn app.main:app --reload
```

API documentation: `http://localhost:8000/docs`

### Mobile

```bash
cd mobile
npm install
npx expo start
```

Scan the QR code with Expo Go.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI, SQLAlchemy, PostgreSQL |
| Auth | JWT (python-jose), bcrypt |
| Mobile | React Native, Expo SDK 50 |
| UI | React Native Paper |
| ML | Pet-ReID-IMAG (ResNeSt) |
| Deploy | Railway (backend), EAS (mobile) |

## Documentation

- [Setup Guide](docs/SETUP.md)
- [API Reference](docs/API.md)
- [Deployment](docs/DEPLOYMENT.md)
- [Architecture](docs/ARCHITECTURE.md)

## ML Model

The `ml_model/` directory contains the Pet-ReID-IMAG model, the 3rd place solution from the CVPR2022 Biometrics Workshop Pet Biometric Challenge. It achieves 91.7% accuracy in pet identification.

## License

Application code: MIT License. See [LICENSE.md](LICENSE.md).

The ML model retains its original license.
