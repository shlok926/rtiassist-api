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
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rtiassist_documents.db"

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
    db.add(auth1)
    db.commit()

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
    
def mock_call_asi1_classifier_food(*args, **kwargs):
    return json.dumps({
        "department": "Food and Public Distribution",
        "ministry": None,
        "government_level": "CENTRAL",
        "state": None,
        "confidence": 0.9
    })
    
def mock_call_asi1_draft(*args, **kwargs):
    return "This is a mock RTI draft application for Food department."
    
def mock_call_asi1_quality(*args, **kwargs):
    return json.dumps({
        "is_valid": True,
        "score": 85,
        "issues": [],
        "suggestions": [],
        "exempt_risk": "low"
    })
    
def mock_call_asi1_quality_fail(*args, **kwargs):
    return json.dumps({
        "is_valid": False,
        "score": 40,
        "issues": ["Needs more detail"],
        "suggestions": [],
        "exempt_risk": "high"
    })

def setup_case_to_authority_resolved():
    res = client.post("/cases", json={"problem_description": "I need help with my ration card."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_recommender):
        client.post(f"/cases/{case_id}/recommend-action")
        client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
        
    with patch("agents.authority_classifier.call_asi1", side_effect=mock_call_asi1_classifier_food):
        res = client.post(f"/cases/{case_id}/resolve-authority")
        assert res.json()["match_status"] == "MATCHED"
        
    return case_id

def test_generate_document_success():
    db = TestingSessionLocal()
    seed_authorities(db)
    db.close()
    
    case_id = setup_case_to_authority_resolved()
    
    with patch("agents.draft_generator.call_asi1", side_effect=mock_call_asi1_draft), \
         patch("agents.quality_checker.call_asi1", side_effect=mock_call_asi1_quality):
        res = client.post(f"/cases/{case_id}/generate-document", json={"language": "english"})
        assert res.status_code == 200
        doc = res.json()
        assert doc["status"] == "READY_TO_FILE"
        assert doc["document_type"] == "RTI"
        assert doc["content"] == "This is a mock RTI draft application for Food department."
        assert doc["version"] == "v1"
        assert doc["quality_score"] == "85"
        
    # Check Case Status
    res = client.get(f"/cases/{case_id}")
    case = res.json()
    assert case["status"] == "READY_TO_FILE"
    
def test_generate_document_needs_revision():
    db = TestingSessionLocal()
    seed_authorities(db)
    db.close()
    
    case_id = setup_case_to_authority_resolved()
    
    with patch("agents.draft_generator.call_asi1", side_effect=mock_call_asi1_draft), \
         patch("agents.quality_checker.call_asi1", side_effect=mock_call_asi1_quality_fail):
        res = client.post(f"/cases/{case_id}/generate-document", json={"language": "english"})
        assert res.status_code == 200
        doc = res.json()
        assert doc["status"] == "NEEDS_REVISION"
        assert doc["quality_score"] == "40"
        
    res = client.get(f"/cases/{case_id}")
    case = res.json()
    assert case["status"] == "DOCUMENT_NEEDS_REVISION"
    
def test_generate_document_unresolved_authority():
    res = client.post("/cases", json={"problem_description": "I need help with my ration card."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_recommender):
        client.post(f"/cases/{case_id}/recommend-action")
        client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
        
    # Do NOT resolve authority
    res = client.post(f"/cases/{case_id}/generate-document", json={"language": "english"})
    assert res.status_code == 400
    assert "Expected AUTHORITY_RESOLVED" in res.json()["detail"]
    
def test_get_document_pdf():
    db = TestingSessionLocal()
    seed_authorities(db)
    db.close()
    
    case_id = setup_case_to_authority_resolved()
    
    with patch("agents.draft_generator.call_asi1", side_effect=mock_call_asi1_draft), \
         patch("agents.quality_checker.call_asi1", side_effect=mock_call_asi1_quality):
        res = client.post(f"/cases/{case_id}/generate-document", json={"language": "english"})
        doc_id = res.json()["id"]
        
    res = client.get(f"/cases/{case_id}/documents/{doc_id}/pdf")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert "attachment; filename=" in res.headers["content-disposition"]
