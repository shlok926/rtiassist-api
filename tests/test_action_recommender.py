import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rtiassist_recommend.db"

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

def mock_call_asi1_rti(*args, **kwargs):
    return json.dumps({
        "recommended_action": "RTI",
        "confidence": 0.95,
        "objective": "Get information",
        "reasoning": ["Seeking records"],
        "alternative_actions": [],
        "missing_information": [],
        "required_documents": [],
        "urgency": "NORMAL",
        "warnings": []
    })
    
def mock_call_asi1_clarification(*args, **kwargs):
    return json.dumps({
        "recommended_action": "NEEDS_CLARIFICATION",
        "confidence": 0.95,
        "objective": "Unknown",
        "reasoning": ["Vague"],
        "alternative_actions": [],
        "missing_information": ["What department?"],
        "required_documents": [],
        "urgency": "NORMAL",
        "warnings": []
    })

def mock_call_asi1_unsupported(*args, **kwargs):
    return json.dumps({
        "recommended_action": "OTHER / UNSUPPORTED",
        "confidence": 0.8,
        "objective": "Appeal decision",
        "reasoning": ["Appeal needed"],
        "alternative_actions": [],
        "missing_information": [],
        "required_documents": [],
        "urgency": "NORMAL",
        "warnings": []
    })
    
def test_recommend_action_success():
    # 1. Create a case
    res = client.post("/cases", json={"problem_description": "My ration card was rejected and I want to know why."})
    case_id = res.json()["id"]
    
    # 2. Recommend action (mocked)
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_rti):
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.status_code == 200
        data = res.json()
        assert data["recommended_action"] == "RTI"
        assert data["supported"] is True
        
    # 3. Check case status
    res = client.get(f"/cases/{case_id}")
    case_data = res.json()
    assert case_data["status"] == "ACTION_RECOMMENDED"
    assert case_data["recommended_action"] == "RTI"
    
    # Verify event
    events = case_data["events"]
    assert len(events) == 2 # CASE_CREATED, ACTION_RECOMMENDED
    assert events[-1]["event_type"] == "ACTION_RECOMMENDED"

def test_recommend_action_clarification():
    res = client.post("/cases", json={"problem_description": "I need help."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_clarification):
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.status_code == 200
        data = res.json()
        assert data["recommended_action"] == "NEEDS_CLARIFICATION"
        
    res = client.get(f"/cases/{case_id}")
    case_data = res.json()
    # Status should remain UNDERSTANDING
    assert case_data["status"] == "UNDERSTANDING"
    assert case_data["recommended_action"] == "NEEDS_CLARIFICATION"
    
    events = case_data["events"]
    assert events[-1]["event_type"] == "ACTION_CLARIFICATION_REQUIRED"

def test_confirm_action():
    res = client.post("/cases", json={"problem_description": "I need help."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_rti):
        client.post(f"/cases/{case_id}/recommend-action")
        
    res = client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
    assert res.status_code == 200
    assert res.json()["status"] == "ACTION_CONFIRMED"
    
    events = res.json()["events"]
    assert events[-1]["event_type"] == "ACTION_CONFIRMED"

def test_confirm_action_invalid_state():
    res = client.post("/cases", json={"problem_description": "I need help."})
    case_id = res.json()["id"]
    
    # Try to confirm BEFORE recommending
    res = client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
    assert res.status_code == 400
    assert "Case must be in ACTION_RECOMMENDED" in res.json()["detail"]

def test_unsupported_action():
    res = client.post("/cases", json={"problem_description": "I want to appeal."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_unsupported):
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.status_code == 200
        assert res.json()["recommended_action"] == "OTHER / UNSUPPORTED"
        assert res.json()["supported"] is False
