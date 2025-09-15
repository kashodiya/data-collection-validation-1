





































import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database and tables
Base.metadata.create_all(bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)

@pytest.fixture
def test_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create test user
    db = TestingSessionLocal()
    user = User(
        username="testuser",
        password_hash=get_password_hash("testpassword"),
        email="test@example.com",
        role="external",
        status="active"
    )
    db.add(user)
    db.commit()
    
    yield db
    
    # Clean up
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_login_success(test_db):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(test_db):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 401
    assert "detail" in response.json()

def test_get_profile(test_db):
    # First login to get token
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    token = login_response.json()["access_token"]
    
    # Use token to get profile
    response = client.get(
        "/api/v1/auth/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"
    assert response.json()["role"] == "external"





































