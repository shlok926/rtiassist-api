import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import get_db, Base
import models.orm
from main import app
from dependencies.auth import get_current_user

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rtiassist_auth.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_auth_env():
    old_env = os.environ.get("ENVIRONMENT")
    os.environ["ENVIRONMENT"] = "production"
    os.environ["JWT_SECRET_KEY"] = "testsecret"
    yield
    if old_env is not None:
        os.environ["ENVIRONMENT"] = old_env
    else:
        del os.environ["ENVIRONMENT"]

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

def test_register_user():
    res = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "password_hash" not in data
    assert data["is_active"] is True

def test_register_duplicate_email():
    client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    res = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert res.status_code == 400
    assert "already registered" in res.json()["detail"]

def test_login_user():
    client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    res = client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_invalid_password():
    client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    res = client.post("/auth/login", json={"email": "test@example.com", "password": "wrongpassword"})
    assert res.status_code == 401

def test_auth_me():
    client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    login_res = client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})
    token = login_res.json()["access_token"]
    
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"

def test_missing_token():
    res = client.get("/auth/me")
    assert res.status_code == 401

def test_expired_or_invalid_token():
    res = client.get("/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
    assert res.status_code == 401

def test_case_ownership():
    # User A
    client.post("/auth/register", json={"email": "userA@example.com", "password": "password123"})
    token_A = client.post("/auth/login", json={"email": "userA@example.com", "password": "password123"}).json()["access_token"]
    
    # User B
    client.post("/auth/register", json={"email": "userB@example.com", "password": "password123"})
    token_B = client.post("/auth/login", json={"email": "userB@example.com", "password": "password123"}).json()["access_token"]
    
    # User A creates a case
    res = client.post("/cases", json={"problem_description": "User A issue"}, headers={"Authorization": f"Bearer {token_A}"})
    assert res.status_code == 200
    case_id_A = res.json()["id"]
    
    # User B attempts to get User A's case
    res_b_get = client.get(f"/cases/{case_id_A}", headers={"Authorization": f"Bearer {token_B}"})
    assert res_b_get.status_code == 404 # Our system returns 404 for not found or access denied
    
    # User A can get it
    res_a_get = client.get(f"/cases/{case_id_A}", headers={"Authorization": f"Bearer {token_A}"})
    assert res_a_get.status_code == 200

def test_admin_authorization():
    # User A (Regular User)
    client.post("/auth/register", json={"email": "regular@example.com", "password": "password123"})
    token_regular = client.post("/auth/login", json={"email": "regular@example.com", "password": "password123"}).json()["access_token"]
    
    # Regular user -> admin endpoint -> DENIED
    res_denied = client.get("/auth/admin-only", headers={"Authorization": f"Bearer {token_regular}"})
    assert res_denied.status_code == 403
    
    # Create an Admin User (by updating DB directly)
    client.post("/auth/register", json={"email": "admin@example.com", "password": "password123"})
    
    db = TestingSessionLocal()
    from models.orm.user import User
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    admin_user.role = "admin"
    db.commit()
    db.close()
    
    token_admin = client.post("/auth/login", json={"email": "admin@example.com", "password": "password123"}).json()["access_token"]
    
    # Admin -> admin endpoint -> ALLOWED
    res_allowed = client.get("/auth/admin-only", headers={"Authorization": f"Bearer {token_admin}"})
    assert res_allowed.status_code == 200
    assert "admin@example.com" in res_allowed.json()["message"]
