













































import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.institution import Institution

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
    
    # Create test users
    db = TestingSessionLocal()
    
    # Admin user
    admin_user = User(
        username="admin",
        password_hash=get_password_hash("adminpassword"),
        email="admin@example.com",
        role="admin",
        status="active"
    )
    
    # External user
    external_user = User(
        username="external",
        password_hash=get_password_hash("externalpassword"),
        email="external@example.com",
        role="external",
        status="active"
    )
    
    # Create test institution
    institution = Institution(
        rssd_id="1234567",
        name="Test Bank",
        institution_type="Commercial Bank",
        contact_info="123 Test St, Test City, TS 12345",
        status="active"
    )
    
    db.add(admin_user)
    db.add(external_user)
    db.add(institution)
    db.commit()
    
    # Update external user with institution ID
    external_user.institution_id = institution.id
    db.commit()
    
    yield db
    
    # Clean up
    db.close()
    Base.metadata.drop_all(bind=engine)

def get_admin_token():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin",
            "password": "adminpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()["access_token"]

def get_external_token():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "external",
            "password": "externalpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()["access_token"]

def test_get_institutions_admin(test_db):
    token = get_admin_token()
    
    response = client.get(
        "/api/v1/institutions/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Bank"

def test_get_institutions_external(test_db):
    token = get_external_token()
    
    response = client.get(
        "/api/v1/institutions/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Bank"

def test_create_institution_admin(test_db):
    token = get_admin_token()
    
    response = client.post(
        "/api/v1/institutions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "rssd_id": "7654321",
            "name": "New Test Bank",
            "institution_type": "State Bank",
            "contact_info": "456 New St, New City, NS 67890",
            "status": "active"
        }
    )
    
    assert response.status_code == 201
    assert response.json()["name"] == "New Test Bank"
    assert response.json()["rssd_id"] == "7654321"

def test_create_institution_external_forbidden(test_db):
    token = get_external_token()
    
    response = client.post(
        "/api/v1/institutions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "rssd_id": "7654321",
            "name": "New Test Bank",
            "institution_type": "State Bank",
            "contact_info": "456 New St, New City, NS 67890",
            "status": "active"
        }
    )
    
    assert response.status_code == 403













































