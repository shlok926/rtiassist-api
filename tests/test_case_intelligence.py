import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_case_intelligence.db"

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

def mock_call_asi1_grievance(*args, **kwargs):
    return json.dumps({
        "recommended_action": "PUBLIC_GRIEVANCE",
        "confidence": 0.95,
        "objective": "Wants the road repaired.",
        "extracted_facts": {
            "department": "Municipal Corporation",
            "location": "Pune"
        },
        "reasoning": ["Seeking a remedy, not information."],
        "alternative_actions": ["RTI"],
        "missing_information": [],
        "required_documents": [],
        "urgency": "NORMAL",
        "warnings": []
    })

def mock_call_asi1_rti(*args, **kwargs):
    return json.dumps({
        "recommended_action": "RTI",
        "confidence": 0.98,
        "objective": "Wants to know why scholarship is delayed.",
        "extracted_facts": {
            "department": "Education Department",
            "application_reference": "SCH-12345"
        },
        "reasoning": ["Seeking official records explaining delay."],
        "alternative_actions": ["PUBLIC_GRIEVANCE"],
        "missing_information": [],
        "required_documents": [],
        "urgency": "NORMAL",
        "warnings": []
    })

def test_grievance_vs_rti_and_structured_facts():
    # 1. Citizen has a grievance
    res = client.post("/cases", json={"problem_description": "The municipality has not repaired the road outside my house for six months."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_grievance):
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.status_code == 200
        data = res.json()
        assert data["recommended_action"] == "PUBLIC_GRIEVANCE"
        assert data["objective"] == "Wants the road repaired."
        assert data["extracted_facts"]["department"] == "Municipal Corporation"
        
    res = client.get(f"/cases/{case_id}")
    case_data = res.json()
    assert case_data["case_objective"] == "Wants the road repaired."
    assert "Municipal Corporation" in case_data["extracted_facts"]
    
    # 2. Citizen wants records
    res2 = client.post("/cases", json={"problem_description": "I want records showing why my scholarship was rejected."})
    case_id2 = res2.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_rti):
        res2 = client.post(f"/cases/{case_id2}/recommend-action")
        assert res2.status_code == 200
        data2 = res2.json()
        assert data2["recommended_action"] == "RTI"
        assert data2["extracted_facts"]["application_reference"] == "SCH-12345"
