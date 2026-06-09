from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings


def create_db_engine():
    """Create engine with appropriate settings for env."""
    if "sqlite" in settings.DATABASE_URL:
        # SQLite for testing — no pool settings
        return create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False}
        )
    # PostgreSQL for production
    return create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )


engine = create_db_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """FastAPI dependency — yields DB session, always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
