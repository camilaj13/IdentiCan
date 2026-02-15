# IdentiCan - Backend

API REST construida con FastAPI para la identificación biométrica canina.

## Requisitos

- Python 3.11+
- PostgreSQL 14+

## Instalación

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Configuración

Copiar `.env.example` a `.env` y configurar las variables:

```bash
cp .env.example .env
```

## Ejecución

```bash
# Desarrollo
uvicorn app.main:app --reload

# O directamente
python app/main.py
```

La documentación interactiva está disponible en `http://localhost:8000/docs`.

## Tests

```bash
pytest tests/ -v
```

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /api/auth/register | Registro |
| POST | /api/auth/login | Login |
| GET | /api/auth/me | Perfil |
| POST | /api/dogs | Crear perro |
| GET | /api/dogs | Listar perros |
| POST | /api/nose/verify | Verificar nariz |
| POST | /api/vaccines | Agregar vacuna |
| GET | /api/qr/generate/{id} | Generar QR PNG |
