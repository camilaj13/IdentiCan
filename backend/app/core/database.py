from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

_connect_args = {}
_engine_kwargs = {
    "pool_pre_ping": True,
}

# SQLite needs special handling (used in tests)
if settings.DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}
else:
    _engine_kwargs["pool_size"] = 10
    _engine_kwargs["max_overflow"] = 20

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    **_engine_kwargs,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
