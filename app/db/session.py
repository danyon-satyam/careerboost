from app.db.database import SessionLocal


def get_session():
    """Utility to get a DB session outside of FastAPI context."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        