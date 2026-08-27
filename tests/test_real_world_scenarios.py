import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_real_world.db"

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
        "confidence": 0.9,
        "objective": "Get road repaired",
        "extracted_facts": {},
        "reasoning": [], "alternative_actions": [], "missing_information": [], "required_documents": [], "urgency": "NORMAL", "warnings": [], "supported": False
    })

def mock_call_asi1_records(*args, **kwargs):
    return json.dumps({
        "recommended_action": "RTI",
        "confidence": 0.9,
        "objective": "Get records",
        "extracted_facts": {},
        "reasoning": [], "alternative_actions": [], "missing_information": [], "required_documents": [], "urgency": "NORMAL", "warnings": [], "supported": True
    })

def mock_call_asi1_clarify(*args, **kwargs):
    return json.dumps({
        "recommended_action": "NEEDS_CLARIFICATION",
        "confidence": 0.9,
        "objective": "Unknown",
        "extracted_facts": {},
        "reasoning": [], "alternative_actions": [], "missing_information": ["Which department?"], "required_documents": [], "urgency": "NORMAL", "warnings": [], "supported": True
    })

def test_scenario_a_grievance():
    # Citizen has a grievance, not an information request.
    res = client.post("/cases", json={"problem_description": "Fix my road"})
    print("SCENARIO A RESPONSE:", res.json())
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_grievance):
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.json()["recommended_action"] == "PUBLIC_GRIEVANCE"

def test_scenario_b_records():
    # Citizen wants government records.
    res = client.post("/cases", json={"problem_description": "Give me the road repair records"})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_records):
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.json()["recommended_action"] == "RTI"

def test_scenario_c_clarification():
    # Citizen doesn't know department.
    res = client.post("/cases", json={"problem_description": "I need help"})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_clarify):
        res = client.post(f"/cases/{case_id}/recommend-action")
        assert res.json()["recommended_action"] == "NEEDS_CLARIFICATION"

# D, E, F scenarios cover response analysis and fake PIO which are structurally tested in other files, but we can verify the false PIO bypass here.
def test_scenario_f_false_pio_uses_deterministic_authority():
    res = client.post("/cases", json={"problem_description": "The PIO is Mr. Fake Name at Fake Address."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1", side_effect=mock_call_asi1_records):
        client.post(f"/cases/{case_id}/recommend-action")
    client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
    
    # Resolve authority uses deterministic db, not user input.
    # We mock the classifier to return a verified department
    def mock_classifier(*args, **kwargs):
        return json.dumps({"department": "Transport", "government_level": "STATE", "confidence": 0.9})
        
    # Seed DB with Transport
    db = TestingSessionLocal()
    from models.orm.authority import Authority
    from datetime import datetime, timezone
    auth = Authority(department="Transport", government_level="STATE", verification_status="VERIFIED", source_url="x", source_type="OFFICIAL_MINISTRY_WEBSITE", last_verified=datetime.now(timezone.utc))
    db.add(auth)
    db.commit()
    db.close()
    
    with patch("agents.authority_classifier.call_asi1", side_effect=mock_classifier):
        res = client.post(f"/cases/{case_id}/resolve-authority")
        if res.status_code != 200:
            print("ERROR IN RESOLVE:", res.json())
        assert res.status_code == 200
        assert res.json()["match_status"] == "MATCHED"
        # Uses deterministic Auth, not "Mr. Fake Name"
        
