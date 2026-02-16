# IdentiCan - Backend

REST API built with FastAPI for canine biometric identification.

## Requirements

- Python 3.11+
- PostgreSQL 14+

## Installation

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure the variables:

```bash
cp .env.example .env
```

## Running

```bash
# Development
uvicorn app.main:app --reload

# Or directly
python app/main.py
```

Interactive documentation is available at `http://localhost:8000/docs`.

## Tests

```bash
pytest tests/ -v
```

## Main Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /api/auth/register | Register |
| POST | /api/auth/login | Login |
| GET | /api/auth/me | Profile |
| POST | /api/dogs | Create dog |
| GET | /api/dogs | List dogs |
| POST | /api/nose/verify | Verify nose |
| POST | /api/vaccines | Add vaccine |
| GET | /api/qr/generate/{id} | Generate QR PNG |
