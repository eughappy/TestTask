import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.config import settings

# Create a new database for testing
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/auth_test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a test client
client = TestClient(app)

# Dependency override for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the database tables before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_user():
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_existing_user():
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass",
        "full_name": "Test User"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_user():
    response = client.post("/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_me():
    login_response = client.post("/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    token = login_response.json()["access_token"]
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
