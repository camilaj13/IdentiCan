# Guía de Instalación - IdentiCan

## Requisitos Previos

### Backend
- Python 3.11+
- PostgreSQL 14+
- pip

### Mobile
- Node.js 18+
- npm o yarn
- Expo Go (app en celular)

---

## Backend

### 1. Clonar y navegar

```bash
git clone https://github.com/camilaj13/IdentiCan.git
cd IdentiCan/backend
```

### 2. Entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus valores reales:
- `DATABASE_URL`: URL de tu base PostgreSQL
- `SECRET_KEY`: Clave secreta única
- `JWT_SECRET`: Clave JWT única

### 5. Crear la base de datos

```bash
# En PostgreSQL
createdb identican
```

Las tablas se crean automáticamente al iniciar la app.

### 6. Ejecutar

```bash
uvicorn app.main:app --reload
```

Abrir `http://localhost:8000/docs` para ver la documentación interactiva.

---

## Mobile

### 1. Navegar al proyecto

```bash
cd IdentiCan/mobile
```

### 2. Instalar dependencias

```bash
npm install
```

### 3. Configurar API URL

Editar `src/constants/config.js` si el backend corre en otra dirección.

### 4. Ejecutar

```bash
npx expo start
```

Escanear el QR con la app Expo Go en tu celular.

---

## Desarrollo con Docker (Backend)

```bash
cd backend
docker build -t identican-backend .
docker run -p 8000:8000 --env-file .env identican-backend
```
