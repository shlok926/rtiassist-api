import pytest
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from integrations.telegram.identity import get_or_create_telegram_user
from models.orm.authority import Authority
from datetime import datetime, timezone

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_parity.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    auth = Authority(id="AUTH-TEST", department="Test Dept", government_level="STATE", verification_status="VERIFIED", source_url="x", source_type="OFFICIAL", last_verified=datetime.now(timezone.utc))
    db.add(auth)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def setup_auth_env():
    import os
    old_env = os.environ.get("ENVIRONMENT")
    os.environ["ENVIRONMENT"] = "production"
    os.environ["JWT_SECRET_KEY"] = "testsecret"
    yield
    if old_env is not None:
        os.environ["ENVIRONMENT"] = old_env
    else:
        del os.environ["ENVIRONMENT"]

def test_web_telegram_parity():
    # TEST A: Register User A on WEB
    res = client.post("/auth/register", json={"email": "userA@example.com", "password": "password123"})
    assert res.status_code in [200, 201]
    
    # Login on Web
    login_res = client.post("/auth/login", json={"email": "userA@example.com", "password": "password123"})
    print("LOGIN RESPONSE:", login_res.status_code, login_res.json())
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create Case on WEB
    res = client.post("/cases", json={"problem_description": "Fix my parity"}, headers=headers)
    assert res.status_code == 200
    case_id = res.json()["id"]
    
    # Get user_id from /auth/me
    me_res = client.get("/auth/me", headers=headers)
    user_id = me_res.json()["id"]
    
    # TELEGRAM: Map same telegram_id to User A
    # Since we don't have a direct route to manually map telegram ID to existing users in this simple test,
    # we'll inject the telegram_id into the DB for User A.
    db = TestingSessionLocal()
    from models.orm.user import User
    user = db.query(User).filter(User.id == user_id).first()
    user.telegram_id = 999999
    db.commit()
    db.close()
    
    # Now Telegram retrieves the same case.
    # In `integrations.telegram.identity`, `get_or_create_user_from_telegram` should fetch User A.
    db = TestingSessionLocal()
    tg_user = get_or_create_telegram_user(db, "999999", "UserA")
    assert tg_user.id == user_id
    db.close()
    
    # TEST B: Action Recommendation Parity
    with patch("agents.action_recommender.call_asi1", return_value=json.dumps({"recommended_action": "RTI", "confidence": 0.9, "objective": "Parity test", "extracted_facts": {}, "reasoning": [], "alternative_actions": [], "missing_information": [], "required_documents": [], "urgency": "NORMAL", "warnings": [], "supported": True})):
        res = client.post(f"/cases/{case_id}/recommend-action", headers=headers)
        assert res.json()["recommended_action"] == "RTI"
        
    # Telegram retrieval parity
    res = client.get(f"/cases/{case_id}", headers=headers)
    web_case = res.json()
    assert web_case["recommended_action"] == "RTI"
    
    # TEST C & D: Modify via Telegram (Simulated via domain service)
    from services.case_service import confirm_action
    from models.schemas import ActionConfirmation
    db = TestingSessionLocal()
    confirm_action(db, case_id, user_id, ActionConfirmation(action="RTI"))
    db.close()
    
    # WEB MUST SEE MODIFICATION
    res = client.get(f"/cases/{case_id}", headers=headers)
    assert res.json()["status"] == "ACTION_CONFIRMED"
    
    # TEST E: Security Isolation
    # Register User B
    res2 = client.post("/auth/register", json={"email": "userB@example.com", "password": "password123"})
    login_res2 = client.post("/auth/login", json={"email": "userB@example.com", "password": "password123"})
    print("USER B LOGIN:", login_res2.status_code, login_res2.text)
    token2 = login_res2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    # User B attempts to access User A's case
    res_b = client.get(f"/cases/{case_id}", headers=headers2)
    assert res_b.status_code == 404 # Isolated
    
    # User B attempts to modify User A's case
    res_b = client.post(f"/cases/{case_id}/recommend-action", headers=headers2)
    assert res_b.status_code == 404
