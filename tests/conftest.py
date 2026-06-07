import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db

# Use SQLite for tests — no PostgreSQL needed in CI
SQLALCHEMY_TEST_URL = "sqlite:///./test_careerboost.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables before tests, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # Note: SQLite file cleanup skipped on Windows due to file lock
    # The file is small and gets overwritten on next test run


@pytest.fixture(scope="function")
def db_session(setup_database):
    """Fresh DB session per test, rolls back after each."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Test client with DB override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_user_data():
    """Sample user payload for tests."""
    return {
        "email": "test@careerboost.com",
        "password": "SecurePass123!",
        "full_name": "Test User"
    }


@pytest.fixture(scope="function")
def registered_user(client, sample_user_data):
    """Creates a user and returns the response data."""
    response = client.post(
        "/api/v1/auth/signup",
        json=sample_user_data
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
def auth_headers(client, sample_user_data, registered_user):
    """Returns Authorization headers with valid JWT token."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
