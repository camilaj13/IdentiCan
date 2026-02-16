from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from contextlib import asynccontextmanager
import logging

from app.api import admin, auth, dogs, nose, payments, qr, vaccines
from app.core.config import settings
from app.core.database import Base, engine

logger = logging.getLogger(__name__)


def _create_tables():
    """Create database tables if they don't exist."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.warning("Could not create tables at startup: %s", e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _create_tables()
    yield


# Also try eagerly so tables exist for TestClient without context manager
_create_tables()


# Rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Canine biometric identification API. "
        "Register your dog, track vaccines, and generate a unique QR code."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(dogs.router)
app.include_router(nose.router)
app.include_router(vaccines.router)
app.include_router(qr.router)
app.include_router(admin.router)
app.include_router(payments.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
