import pytest
from fastapi.testclient import TestClient
from main import app
from models.database import engine, Base, SessionLocal
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from models.orm.authority import Authority
from utils.config import AUTHORITY_VERIFICATION_MAX_AGE_DAYS
from models.orm.user import User

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    import models.orm
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def admin_token():
    db = SessionLocal()
    admin = User(email="admin@test.com", password_hash="hash", is_active=True, role="admin")
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    from jose import jwt
    from utils.config import JWT_SECRET_KEY, JWT_ALGORITHM
    token = jwt.encode({"sub": admin.id}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    db.close()
    return token

@pytest.fixture
def user_token():
    db = SessionLocal()
    user = User(email="user@test.com", password_hash="hash", is_active=True, role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    from jose import jwt
    from utils.config import JWT_SECRET_KEY, JWT_ALGORITHM
    token = jwt.encode({"sub": user.id}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    db.close()
    return token

def test_admin_create_authority(admin_token):
    response = client.post(
        "/admin/authorities",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "department": "Transport",
            "government_level": "STATE",
            "source_url": "http://transport.test",
            "source_type": "OFFICIAL_GOVERNMENT_WEBSITE",
            "state": "MH"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["department"] == "Transport"
    assert data["verification_status"] == "UNVERIFIED"

def test_user_cannot_create_authority(user_token):
    response = client.post(
        "/admin/authorities",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "department": "Transport",
            "government_level": "STATE",
            "source_url": "http://transport.test",
            "source_type": "OFFICIAL_GOVERNMENT_WEBSITE"
        }
    )
    assert response.status_code == 403

def test_admin_verify_and_history(admin_token):
    # 1. Create
    resp1 = client.post(
        "/admin/authorities",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "department": "Police",
            "government_level": "STATE",
            "source_url": "http://police.test",
            "source_type": "OTHER"
        }
    )
    auth_id = resp1.json()["id"]
    
    # 2. Verify
    resp2 = client.post(
        f"/admin/authorities/{auth_id}/verify",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "source_url": "http://police.official.test",
            "source_type": "OFFICIAL_GOVERNMENT_WEBSITE",
            "notes": "Verified by phone call"
        }
    )
    assert resp2.status_code == 200
    assert resp2.json()["verification_status"] == "VERIFIED"
    
    # 3. Check history
    resp3 = client.get(
        f"/admin/authorities/{auth_id}/history",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp3.status_code == 200
    history = resp3.json()
    assert len(history) == 1
    assert history[0]["verification_status"] == "VERIFIED"
    assert history[0]["notes"] == "Verified by phone call"

def test_admin_update_verified_enters_needs_review(admin_token):
    # Create with notes to auto-verify
    resp1 = client.post(
        "/admin/authorities",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "department": "Water",
            "government_level": "CITY",
            "source_url": "http://water.test",
            "source_type": "OFFICIAL_GOVERNMENT_WEBSITE",
            "verification_notes": "Looks good"
        }
    )
    auth_id = resp1.json()["id"]
    assert resp1.json()["verification_status"] == "VERIFIED"
    
    # Update (acting as UNVERIFIED data coming in)
    resp2 = client.patch(
        f"/admin/authorities/{auth_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "address": "New Office"
        }
    )
    assert resp2.status_code == 200
    assert resp2.json()["verification_status"] == "NEEDS_REVIEW"
    assert resp2.json()["address"] == "New Office"

def test_lazy_expiry(admin_token):
    db = SessionLocal()
    # Create manually to spoof last_verified
    auth = Authority(
        department="Expired Dept",
        government_level="STATE",
        source_url="http://expired.test",
        source_type="OTHER",
        verification_status="VERIFIED",
        last_verified=datetime.now(timezone.utc) - timedelta(days=AUTHORITY_VERIFICATION_MAX_AGE_DAYS + 10)
    )
    db.add(auth)
    db.commit()
    db.refresh(auth)
    db.close()
    
    # Fetch using search (should trigger lazy expiry)
    resp = client.get(
        "/authorities/search",
        params={"department": "Expired Dept"}
    )
    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 1
    assert resp.json()["results"][0]["verification_status"] == "EXPIRED"

def test_admin_unverify(admin_token):
    # Create with notes to auto-verify
    resp1 = client.post(
        "/admin/authorities",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "department": "Fire",
            "government_level": "CITY",
            "source_url": "http://fire.test",
            "source_type": "OFFICIAL_GOVERNMENT_WEBSITE",
            "verification_notes": "Initial"
        }
    )
    auth_id = resp1.json()["id"]
    
    # Unverify
    resp2 = client.post(
        f"/admin/authorities/{auth_id}/unverify",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "reason": "Link is dead",
            "new_status": "EXPIRED"
        }
    )
    assert resp2.status_code == 200
    assert resp2.json()["verification_status"] == "EXPIRED"
    
    # Check history
    resp3 = client.get(f"/admin/authorities/{auth_id}/history", headers={"Authorization": f"Bearer {admin_token}"})
    history = resp3.json()
    assert len(history) == 2
    assert history[0]["verification_status"] == "EXPIRED"
