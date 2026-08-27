import pytest
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models.orm.authority import Authority
from datetime import datetime, timezone, timedelta

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_phase15.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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
    db = TestingSessionLocal()
    # Seed authorities
    auth_muni = Authority(id="AUTH-MUNI-1", department="Municipal Corporation", government_level="STATE", verification_status="VERIFIED", source_url="x", source_type="OFFICIAL", last_verified=datetime.now(timezone.utc))
    auth_edu1 = Authority(id="AUTH-EDU-1", department="Education Dept", government_level="STATE", verification_status="VERIFIED", source_url="x", source_type="OFFICIAL", last_verified=datetime.now(timezone.utc))
    auth_edu2 = Authority(id="AUTH-EDU-2", department="Education Dept", government_level="CENTRAL", verification_status="VERIFIED", source_url="x", source_type="OFFICIAL", last_verified=datetime.now(timezone.utc))
    auth_expired = Authority(id="AUTH-EXP", department="Expired Dept", government_level="STATE", verification_status="VERIFIED", source_url="x", source_type="OFFICIAL", last_verified=datetime.now(timezone.utc) - timedelta(days=200))
    
    db.add_all([auth_muni, auth_edu1, auth_edu2, auth_expired])
    db.commit()
    db.close()
    
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

def mock_llm_response(recommended_action, objective, facts, missing=None, supported=True):
    return json.dumps({
        "recommended_action": recommended_action,
        "confidence": 0.95,
        "objective": objective,
        "extracted_facts": facts,
        "reasoning": ["Mock reasoning"],
        "alternative_actions": [],
        "missing_information": missing or [],
        "required_documents": [],
        "urgency": "NORMAL",
        "warnings": [],
        "supported": supported
    })

def test_01_pure_information_request():
    with patch("agents.action_recommender.call_asi1", return_value=mock_llm_response("RTI", "Get budget records", {"ward": "Andheri"})):
        res = client.post("/cases", json={"problem_description": "I want a copy of the approved budget and expenditure records for the municipal road project in my ward."})
        assert res.status_code == 200
        case_id = res.json()["id"]
        
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.status_code == 200
        assert res.json()["recommended_action"] == "RTI"

def test_02_grievance_not_rti():
    with patch("agents.action_recommender.call_asi1", return_value=mock_llm_response("PUBLIC_GRIEVANCE", "Repair road", {}, supported=False)):
        res = client.post("/cases", json={"problem_description": "The road outside my house has been damaged for six months. I want the municipality to repair it."})
        case_id = res.json()["id"]
        
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.status_code == 200
        assert res.json()["recommended_action"] == "PUBLIC_GRIEVANCE"
        assert res.json()["supported"] is False

def test_03_grievance_and_information():
    with patch("agents.action_recommender.call_asi1", return_value=mock_llm_response("RTI", "Know status of scholarship", {"issue": "delay"})):
        res = client.post("/cases", json={"problem_description": "My scholarship has not been credited. I want the payment processed and also want to know the current status and reason for the delay."})
        case_id = res.json()["id"]
        
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.status_code == 200
        assert res.json()["recommended_action"] == "RTI"

def test_04_unknown_department():
    with patch("agents.action_recommender.call_asi1", return_value=mock_llm_response("NEEDS_CLARIFICATION", "Unknown", {}, missing=["Scheme name"])):
        res = client.post("/cases", json={"problem_description": "I applied for a government scheme but I don't know which department handles it."})
        case_id = res.json()["id"]
        
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.status_code == 200
        assert res.json()["recommended_action"] == "NEEDS_CLARIFICATION"

def test_06_incorrect_pio_provided():
    with patch("agents.action_recommender.call_asi1", return_value=mock_llm_response("RTI", "Get info", {"pio": "Mr. XYZ"})):
        res = client.post("/cases", json={"problem_description": "The PIO is Mr. XYZ at this address."})
        case_id = res.json()["id"]
        client.post(f"/cases/{case_id}/recommend-action")
        client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
        
        with patch("agents.authority_classifier.call_asi1", return_value=json.dumps({"department": "Municipal Corporation", "government_level": "STATE", "confidence": 0.9})):
            res = client.post(f"/cases/{case_id}/resolve-authority")
            assert res.status_code == 200
            assert res.json()["match_status"] == "MATCHED"
            assert res.json()["authority_id"] == "AUTH-MUNI-1"

def test_07_ambiguous_authority():
    res = client.post("/cases", json={"problem_description": "I need records from the education department."})
    case_id = res.json()["id"]
    with patch("agents.action_recommender.call_asi1", return_value=mock_llm_response("RTI", "Get info", {})):
        client.post(f"/cases/{case_id}/recommend-action")
    client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
    
    with patch("agents.authority_classifier.call_asi1", return_value=json.dumps({"department": "Education Dept", "government_level": None, "confidence": 0.5})):
        res = client.post(f"/cases/{case_id}/resolve-authority")
        assert res.status_code == 200
        assert res.json()["match_status"] in ["MULTIPLE_MATCHES", "NEEDS_REVIEW", "AUTHORITY_REVIEW_REQUIRED"]

def test_08_verified_authority_expired():
    res = client.post("/cases", json={"problem_description": "Expired department request."})
    case_id = res.json()["id"]
    with patch("agents.action_recommender.call_asi1", return_value=mock_llm_response("RTI", "Get info", {})):
        client.post(f"/cases/{case_id}/recommend-action")
    client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
    
    with patch("agents.authority_classifier.call_asi1", return_value=json.dumps({"department": "Expired Dept", "government_level": "STATE", "confidence": 0.9})):
        res = client.post(f"/cases/{case_id}/resolve-authority")
        assert res.status_code == 200
        assert res.json()["match_status"] in ["EXPIRED", "NEEDS_REVIEW"]

def test_11_complete_government_response():
    # ... mock the analysis flow
    pass

def test_14_user_corrects_ai_understanding():
    res = client.post("/cases", json={"problem_description": "Transport problem"})
    case_id = res.json()["id"]
    client.patch(f"/cases/{case_id}", json={"case_objective": "Municipal Corporation problem"})
    
    res = client.get(f"/cases/{case_id}")
    assert res.json()["case_objective"] == "Municipal Corporation problem"
