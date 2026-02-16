# Setup Guide - IdentiCan

## Prerequisites

### Backend
- Python 3.11+
- PostgreSQL 14+
- pip

### Mobile
- Node.js 18+
- npm or yarn
- Expo Go (app on your phone)

---

## Backend

### 1. Clone and navigate

```bash
git clone https://github.com/camilaj13/IdentiCan.git
cd IdentiCan/backend
```

### 2. Virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- `DATABASE_URL`: Your PostgreSQL URL
- `SECRET_KEY`: Unique secret key
- `JWT_SECRET`: Unique JWT key

### 5. Create the database

```bash
# In PostgreSQL
createdb identican
```

Tables are created automatically when the app starts.

### 6. Run

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` to view the interactive documentation.

---

## Mobile

### 1. Navigate to the project

```bash
cd IdentiCan/mobile
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure API URL

Edit `src/constants/config.js` if the backend runs at a different address.

### 4. Run

```bash
npx expo start
```

Scan the QR code with the Expo Go app on your phone.

---

## Development with Docker (Backend)

```bash
cd backend
docker build -t identican-backend .
docker run -p 8000:8000 --env-file .env identican-backend
```
