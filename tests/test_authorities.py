import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models.orm.authority import Authority
from datetime import datetime, timezone

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rtiassist_authorities.db"

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

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

def seed_authorities(db):
    auth1 = Authority(
        government_level="CENTRAL",
        department="Food and Public Distribution",
        ministry="Consumer Affairs, Food and Public Distribution",
        source_url="https://dfpd.gov.in/rti",
        source_type="OFFICIAL_MINISTRY_WEBSITE",
        last_verified=datetime.now(timezone.utc),
        verification_status="VERIFIED"
    )
    auth2 = Authority(
        government_level="STATE",
        state="Maharashtra",
        department="Transport",
        source_url="https://transport.maharashtra.gov.in",
        source_type="OFFICIAL_DEPARTMENT_WEBSITE",
        last_verified=datetime.now(timezone.utc),
        verification_status="NEEDS_REVIEW"
    )
    db.add(auth1)
    db.add(auth2)
    db.commit()

def test_authority_search():
    db = TestingSessionLocal()
    seed_authorities(db)
    db.close()
    
    res = client.get("/authorities/search?department=Food")
    assert res.status_code == 200
    data = res.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["department"] == "Food and Public Distribution"
    
def mock_call_asi1_classifier_food(*args, **kwargs):
    return json.dumps({
        "department": "Food and Public Distribution",
        "ministry": None,
        "government_level": "CENTRAL",
        "state": None,
        "confidence": 0.9
    })

def mock_call_asi1_classifier_transport(*args, **kwargs):
    return json.dumps({
        "department": "Transport",
        "ministry": None,
        "government_level": "STATE",
        "state": "Maharashtra",
        "confidence": 0.85
    })

def mock_call_asi1_classifier_unknown(*args, **kwargs):
    return json.dumps({
        "department": "Space Force",
        "ministry": None,
        "government_level": "CENTRAL",
        "state": None,
        "confidence": 0.5
    })
    
def mock_call_asi1_recommender(*args, **kwargs):
    return json.dumps({
        "recommended_action": "RTI",
        "confidence": 0.9,
        "objective": "Get info",
        "reasoning": [],
        "alternative_actions": [],
        "missing_information": [],
        "required_documents": [],
        "urgency": "NORMAL",
        "supported": True,
        "warnings": []
    })

def setup_case():
    res = client.post("/cases", json={"problem_description": "I need help."})
    case_id = res.json()["id"]
    
    # Needs overrides since setup_case is a helper
    app.dependency_overrides[get_db] = override_get_db
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_recommender):
        client.post(f"/cases/{case_id}/recommend-action")
        client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
    return case_id

def test_resolve_authority_matched():
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    seed_authorities(db)
    db.close()
    
    case_id = setup_case()
    
    with patch("agents.authority_classifier.call_asi1", side_effect=mock_call_asi1_classifier_food):
        res = client.post(f"/cases/{case_id}/resolve-authority")
        assert res.status_code == 200
        data = res.json()
        assert data["match_status"] == "MATCHED"
        assert data["authority_id"] is not None

def test_resolve_authority_needs_review():
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    seed_authorities(db)
    db.close()
    
    case_id = setup_case()
    
    with patch("agents.authority_classifier.call_asi1", side_effect=mock_call_asi1_classifier_transport):
        res = client.post(f"/cases/{case_id}/resolve-authority")
        assert res.status_code == 200
        data = res.json()
        assert data["match_status"] == "NEEDS_REVIEW"
        assert data["authority_id"] is not None

def test_resolve_authority_no_match():
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    seed_authorities(db)
    db.close()
    
    case_id = setup_case()
    
    with patch("agents.authority_classifier.call_asi1", side_effect=mock_call_asi1_classifier_unknown):
        res = client.post(f"/cases/{case_id}/resolve-authority")
        assert res.status_code == 200
        data = res.json()
        assert data["match_status"] == "NO_MATCH"
        assert data["authority_id"] is None
