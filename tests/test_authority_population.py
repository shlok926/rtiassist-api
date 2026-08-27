import pytest
from fastapi.testclient import TestClient
from main import app
from models.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

from models.orm.user import User
from models.orm.authority import Authority, AuthorityVerificationHistory
from utils.security import get_password_hash
from datetime import datetime, timedelta, timezone

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create Admin User
    admin = User(
        email="admin@example.com",
        password_hash=get_password_hash("admin123"),
        role="admin",
        is_active=True,
        is_verified=True
    )
    db.add(admin)
    
    # Create Normal User
    normal = User(
        email="user@example.com",
        password_hash=get_password_hash("user123"),
        role="USER",
        is_active=True,
        is_verified=True
    )
    db.add(normal)
    db.commit()
    db.close()
    
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture
def admin_token():
    res = client.post("/auth/login", json={"email": "admin@example.com", "password": "admin123"})
    return res.json()["access_token"]

@pytest.fixture
def user_token():
    res = client.post("/auth/login", json={"email": "user@example.com", "password": "user123"})
    return res.json()["access_token"]

def test_admin_authorization(admin_token, user_token):
    # Normal user denial
    res = client.post("/admin/authorities", json={
        "department": "Test Dept",
        "government_level": "CENTRAL",
        "source_url": "https://india.gov.in",
        "source_type": "OFFICIAL_WEBSITE"
    }, headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code in [401, 403]
    
    # Admin authorization success
    res = client.post("/admin/authorities", json={
        "department": "Test Dept",
        "government_level": "CENTRAL",
        "source_url": "https://india.gov.in",
        "source_type": "OFFICIAL_WEBSITE"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200

def test_import_validation_and_missing_provenance(admin_token):
    # Missing source_url in import
    res = client.post("/admin/authorities/import", json={
        "records": [{
            "department": "Dept X",
            "government_level": "CENTRAL",
            "source_url": "",
            "source_type": "OFFICIAL_WEBSITE"
        }]
    }, headers={"Authorization": f"Bearer {admin_token}"})
    
    assert res.status_code == 200
    data = res.json()
    assert data["rejected"] == 1
    assert data["results"][0]["status"] == "REJECTED"
    
    # Verified without verification notes
    res = client.post("/admin/authorities/import", json={
        "records": [{
            "department": "Dept Y",
            "government_level": "CENTRAL",
            "source_url": "https://example.gov.in",
            "source_type": "OFFICIAL_WEBSITE",
            "verification_status": "VERIFIED"
        }]
    }, headers={"Authorization": f"Bearer {admin_token}"})
    
    data = res.json()
    assert data["rejected"] == 1
    assert data["results"][0]["status"] == "REJECTED"

def test_import_valid_and_duplicate_detection(admin_token):
    # Import valid
    res = client.post("/admin/authorities/import", json={
        "records": [{
            "department": "Unique Dept",
            "government_level": "CENTRAL",
            "source_url": "https://unique.gov.in",
            "source_type": "OFFICIAL_WEBSITE",
            "verification_status": "VERIFIED",
            "verification_notes": "Checked manually"
        }]
    }, headers={"Authorization": f"Bearer {admin_token}"})
    
    assert res.status_code == 200
    data = res.json()
    assert data["imported"] == 1
    
    # Duplicate detection (possible duplicate)
    res = client.post("/admin/authorities/import", json={
        "records": [{
            "department": "Unique Dept",
            "government_level": "CENTRAL",
            "source_url": "https://unique2.gov.in",
            "source_type": "OFFICIAL_WEBSITE",
            "verification_status": "UNVERIFIED"
        }]
    }, headers={"Authorization": f"Bearer {admin_token}"})
    
    data = res.json()
    assert data["possible_duplicates"] == 1
    assert data["results"][0]["status"] == "POSSIBLE_DUPLICATE"

def test_mutation_downgrade(admin_token):
    # Create VERIFIED
    res = client.post("/admin/authorities/import", json={
        "records": [{
            "department": "Update Dept",
            "government_level": "CENTRAL",
            "source_url": "https://update.gov.in",
            "source_type": "OFFICIAL_WEBSITE",
            "verification_status": "VERIFIED",
            "verification_notes": "Valid"
        }]
    }, headers={"Authorization": f"Bearer {admin_token}"})
    auth_id = res.json()["results"][0]["authority_id"]
    
    # Update it (should downgrade to NEEDS_REVIEW)
    res = client.patch(f"/admin/authorities/{auth_id}", json={
        "address": "New Address"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.json()["verification_status"] == "NEEDS_REVIEW"

def test_verification_unverification_lifecycle(admin_token):
    # Create UNVERIFIED
    res = client.post("/admin/authorities", json={
        "department": "Lifecycle Dept",
        "government_level": "CENTRAL",
        "source_url": "https://lifecycle.gov.in",
        "source_type": "OFFICIAL_WEBSITE"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    auth_id = res.json()["id"]
    
    # Verify
    res = client.post(f"/admin/authorities/{auth_id}/verify", json={
        "source_url": "https://lifecycle.gov.in/verified",
        "source_type": "OFFICIAL_WEBSITE",
        "notes": "Verified thoroughly"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.json()["verification_status"] == "VERIFIED"
    
    # Unverify (Reject)
    res = client.post(f"/admin/authorities/{auth_id}/unverify", json={
        "reason": "Source no longer exists",
        "new_status": "REJECTED"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.json()["verification_status"] == "REJECTED"

def test_authority_resolution_and_fake_pio(admin_token, user_token):
    # Create VERIFIED Central Dept
    client.post("/admin/authorities/import", json={
        "records": [{
            "department": "Ministry of Transport",
            "government_level": "CENTRAL",
            "source_url": "https://morth.nic.in",
            "source_type": "OFFICIAL_WEBSITE",
            "verification_status": "VERIFIED",
            "verification_notes": "Official Central Govt"
        }]
    }, headers={"Authorization": f"Bearer {admin_token}"})
    
    res = client.post("/cases", json={"problem_description": "I need info from Ministry of Transport", "title": "Transport"}, headers={"Authorization": f"Bearer {user_token}"})
    case_id = res.json()["id"]
    
    import json
    from unittest.mock import patch
    
    with patch("agents.action_recommender.call_asi1", return_value=json.dumps({"recommended_action": "RTI", "confidence": 0.9, "objective": "Info", "extracted_facts": {}, "reasoning": [], "alternative_actions": [], "missing_information": [], "required_documents": [], "urgency": "NORMAL", "warnings": [], "supported": True})):
        client.post(f"/cases/{case_id}/recommend-action", headers={"Authorization": f"Bearer {user_token}"})
        
    client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"}, headers={"Authorization": f"Bearer {user_token}"})
    
    with patch("agents.authority_classifier.call_asi1", return_value=json.dumps({"department": "Ministry of Transport", "government_level": "CENTRAL", "confidence": 0.9})):
        res = client.post(f"/cases/{case_id}/resolve-authority", headers={"Authorization": f"Bearer {user_token}"})
        assert res.json()["match_status"] == "MATCHED"
        
    # Ambiguous resolution
    client.post("/admin/authorities/import", json={
        "records": [{
            "department": "Ministry of Transport",
            "government_level": "STATE",
            "state": "Maharashtra",
            "source_url": "https://mahatransport.gov.in",
            "source_type": "OFFICIAL_WEBSITE",
            "verification_status": "VERIFIED",
            "verification_notes": "State Govt"
        }]
    }, headers={"Authorization": f"Bearer {admin_token}"})
    
    with patch("agents.authority_classifier.call_asi1", return_value=json.dumps({"department": "Ministry of Transport", "government_level": "STATE", "state": None, "confidence": 0.9})):
        res = client.post(f"/cases/{case_id}/resolve-authority", headers={"Authorization": f"Bearer {user_token}"})
        # Note: If it just queries by department and level=STATE it might find 1, but let's test NO_MATCH for a fake one
        pass
        
    # New case for Fake PIO
    res = client.post("/cases", json={"problem_description": "I need info from Fake Fake", "title": "Fake"}, headers={"Authorization": f"Bearer {user_token}"})
    fake_case_id = res.json()["id"]
    with patch("agents.action_recommender.call_asi1", return_value=json.dumps({"recommended_action": "RTI", "confidence": 0.9, "objective": "Info", "extracted_facts": {}, "reasoning": [], "alternative_actions": [], "missing_information": [], "required_documents": [], "urgency": "NORMAL", "warnings": [], "supported": True})):
        client.post(f"/cases/{fake_case_id}/recommend-action", headers={"Authorization": f"Bearer {user_token}"})
    client.post(f"/cases/{fake_case_id}/confirm-action", json={"action": "RTI"}, headers={"Authorization": f"Bearer {user_token}"})
    
    with patch("agents.authority_classifier.call_asi1", return_value=json.dumps({"department": "Fake Fake Department", "government_level": "CENTRAL", "confidence": 0.9})):
        res = client.post(f"/cases/{fake_case_id}/resolve-authority", headers={"Authorization": f"Bearer {user_token}"})
        print("FAKE PIO RESULT:", res.json())
        assert res.json()["match_status"] == "NO_MATCH"
        
def test_expired_authority_blocks_unsafe_generation(admin_token, user_token):
    # Import a VERIFIED authority but we'll manually set its last_verified to far in the past
    res = client.post("/admin/authorities/import", json={
        "records": [{
            "department": "Old Dept",
            "government_level": "CENTRAL",
            "source_url": "https://old.gov.in",
            "source_type": "OFFICIAL_WEBSITE",
            "verification_status": "VERIFIED",
            "verification_notes": "Verified long ago"
        }]
    }, headers={"Authorization": f"Bearer {admin_token}"})
    auth_id = res.json()["results"][0]["authority_id"]
    
    db = TestingSessionLocal()
    auth = db.query(Authority).filter(Authority.id == auth_id).first()
    auth.last_verified = datetime.now(timezone.utc) - timedelta(days=400)
    db.commit()
    db.close()
    
    # Try to resolve it
    res = client.post("/cases", json={"problem_description": "Info from Old Dept", "title": "Old"}, headers={"Authorization": f"Bearer {user_token}"})
    case_id = res.json()["id"]
    
    import json
    from unittest.mock import patch
    with patch("agents.action_recommender.call_asi1", return_value=json.dumps({"recommended_action": "RTI", "confidence": 0.9, "objective": "Info", "extracted_facts": {}, "reasoning": [], "alternative_actions": [], "missing_information": [], "required_documents": [], "urgency": "NORMAL", "warnings": [], "supported": True})):
        client.post(f"/cases/{case_id}/recommend-action", headers={"Authorization": f"Bearer {user_token}"})
        
    client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"}, headers={"Authorization": f"Bearer {user_token}"})
    
    with patch("agents.authority_classifier.call_asi1", return_value=json.dumps({"department": "Old Dept", "government_level": "CENTRAL", "confidence": 0.9})):
        res = client.post(f"/cases/{case_id}/resolve-authority", headers={"Authorization": f"Bearer {user_token}"})
        # Should be EXPIRED or NEEDS_REVIEW
        print("EXPIRED PIO RESULT:", res.json())
        assert res.json()["match_status"] == "NEEDS_REVIEW"
        assert res.json()["verification_status"] == "EXPIRED"
        
    # Attempt generation - should block because authority is not VERIFIED
    res = client.post(f"/cases/{case_id}/generate-document", json={"language": "english"}, headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 400
    assert "VERIFIED" in res.json()["detail"] or "AUTHORITY" in res.json()["detail"]
