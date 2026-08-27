import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from datetime import date, timedelta, datetime, timezone

from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rtiassist_filings.db"

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

def setup_ready_to_file_case():
    # Bypass all the API calls and directly create the state needed
    # Or just use the API flow to ensure realism
    from models.orm.authority import Authority
    db = TestingSessionLocal()
    auth = Authority(
        government_level="CENTRAL",
        department="Test",
        source_url="http://test.gov.in",
        source_type="OFFICIAL_MINISTRY_WEBSITE",
        last_verified=datetime.now(timezone.utc),
        verification_status="VERIFIED"
    )
    db.add(auth)
    db.commit()
    db.close()
    
    # 1. Create Case
    res = client.post("/cases", json={"problem_description": "Need info"})
    case_id = res.json()["id"]
    
    # 2. Recommend and Confirm
    with patch("agents.action_recommender.call_asi1") as mock_asi1:
        mock_asi1.return_value = json.dumps({
            "recommended_action": "RTI", "confidence": 0.9, "objective": "", "reasoning": [],
            "alternative_actions": [], "missing_information": [], "required_documents": [],
            "urgency": "NORMAL", "supported": True, "warnings": []
        })
        client.post(f"/cases/{case_id}/recommend-action")
        client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
        
    # 3. Resolve Authority
    with patch("agents.authority_classifier.call_asi1") as mock_asi1:
        mock_asi1.return_value = json.dumps({
            "department": "Test", "ministry": None, "government_level": "CENTRAL",
            "state": None, "confidence": 0.9
        })
        client.post(f"/cases/{case_id}/resolve-authority")
        
    # 4. Generate Document -> READY_TO_FILE
    with patch("agents.draft_generator.call_asi1") as mock_draft, \
         patch("agents.quality_checker.call_asi1") as mock_qc:
        mock_draft.return_value = "Draft Text"
        mock_qc.return_value = json.dumps({
            "is_valid": True, "score": 90, "issues": [], "suggestions": [], "exempt_risk": "low"
        })
        client.post(f"/cases/{case_id}/generate-document", json={"language": "english"})
        
    return case_id

def test_successful_filing():
    case_id = setup_ready_to_file_case()
    
    filing_date = str(date.today())
    payload = {
        "filing_date": filing_date,
        "filing_method": "ONLINE",
        "reference_number": "12345"
    }
    
    res = client.post(f"/cases/{case_id}/file", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["filing_date"] == filing_date
    assert data["filing_method"] == "ONLINE"
    assert data["reference_number"] == "12345"
    
def test_invalid_state_filing():
    res = client.post("/cases", json={"problem_description": "Need info"})
    case_id = res.json()["id"]
    
    payload = {
        "filing_date": str(date.today()),
        "filing_method": "ONLINE"
    }
    res = client.post(f"/cases/{case_id}/file", json=payload)
    assert res.status_code == 400
    assert "READY_TO_FILE" in res.json()["detail"]

def test_invalid_date_filing():
    case_id = setup_ready_to_file_case()
    
    future_date = str(date.today() + timedelta(days=5))
    payload = {
        "filing_date": future_date,
        "filing_method": "ONLINE"
    }
    res = client.post(f"/cases/{case_id}/file", json=payload)
    assert res.status_code == 400
    assert "cannot be in the future" in res.json()["detail"]

def test_duplicate_filing():
    case_id = setup_ready_to_file_case()
    
    payload = {
        "filing_date": str(date.today()),
        "filing_method": "ONLINE"
    }
    client.post(f"/cases/{case_id}/file", json=payload)
    
    res = client.post(f"/cases/{case_id}/file", json=payload)
    assert res.status_code == 400
    assert "Expected READY_TO_FILE" in res.json()["detail"]

def test_case_timeline():
    case_id = setup_ready_to_file_case()
    payload = {
        "filing_date": str(date.today()),
        "filing_method": "ONLINE"
    }
    client.post(f"/cases/{case_id}/file", json=payload)
    
    res = client.get(f"/cases/{case_id}/timeline")
    assert res.status_code == 200
    data = res.json()
    
    assert data["filing"] is not None
    assert data["filing"]["filing_method"] == "ONLINE"
    assert len(data["deadlines"]) == 1
    assert data["deadlines"][0]["deadline_type"] == "RTI_RESPONSE"
    assert data["deadlines"][0]["status"] in ["UPCOMING", "DUE_SOON", "OVERDUE"]
    assert data["remaining_days"] == 30
    assert data["current_status"] == "AWAITING_RESPONSE"
    
def test_case_list_summary_fields():
    case_id = setup_ready_to_file_case()
    payload = {
        "filing_date": str(date.today()),
        "filing_method": "ONLINE"
    }
    client.post(f"/cases/{case_id}/file", json=payload)
    
    res = client.get("/cases")
    assert res.status_code == 200
    cases = res.json()["cases"]
    
    assert len(cases) > 0
    filed_case = cases[0]
    assert filed_case["filing_date"] == str(date.today())
    assert filed_case["remaining_days"] == 30
    assert filed_case["overdue"] is False
