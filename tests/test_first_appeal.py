import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from datetime import date, datetime, timezone

from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from tests.test_response_analysis import setup_filed_case, create_fake_pdf

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rtiassist_first_appeal.db"

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

def setup_analysis_ready_case():
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
    
    res = client.post("/cases", json={"problem_description": "My complaint was ignored."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1") as mock_asi1:
        mock_asi1.return_value = json.dumps({
            "recommended_action": "RTI", "confidence": 0.9, "objective": "", "reasoning": [],
            "alternative_actions": [], "missing_information": [], "required_documents": [],
            "urgency": "NORMAL", "supported": True, "warnings": []
        })
        client.post(f"/cases/{case_id}/recommend-action")
        client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
        
    with patch("agents.authority_classifier.call_asi1") as mock_asi1:
        mock_asi1.return_value = json.dumps({
            "department": "Test", "ministry": None, "government_level": "CENTRAL",
            "state": None, "confidence": 0.9
        })
        client.post(f"/cases/{case_id}/resolve-authority")
        
    with patch("agents.draft_generator.call_asi1") as mock_draft, \
         patch("agents.quality_checker.call_asi1") as mock_qc:
        mock_draft.return_value = "Draft Text about complaint"
        mock_qc.return_value = json.dumps({
            "is_valid": True, "score": 90, "issues": [], "suggestions": [], "exempt_risk": "low"
        })
        client.post(f"/cases/{case_id}/generate-document", json={"language": "english"})
        
    payload = {
        "filing_date": str(date.today()),
        "filing_method": "ONLINE"
    }
    client.post(f"/cases/{case_id}/file", json=payload)
    
    pdf_bytes = bytes(create_fake_pdf(), "latin1")
    mock_llm_response = json.dumps({
        "status": "PARTIALLY_ANSWERED",
        "answered": ["Complaint forwarded"],
        "not_answered": ["Action taken"],
        "recommended_action": "FIRST_APPEAL",
        "request_mapping": []
    })
    
    with patch("agents.response_analyzer.call_asi1") as mock_llm:
        mock_llm.return_value = mock_llm_response
        client.post(
            f"/cases/{case_id}/responses",
            files={"file": ("response.pdf", pdf_bytes, "application/pdf")}
        )
        
    return case_id

def test_first_appeal_full_workflow():
    case_id = setup_analysis_ready_case()
    
    # 1. Confirm Appeal
    res = client.post(f"/cases/{case_id}/confirm-appeal", json={"appeal_type": "FIRST_APPEAL"})
    assert res.status_code == 200
    appeal_id = res.json()["id"]
    assert res.json()["status"] == "CONFIRMED"
    
    # 2. Resolve Authority
    res = client.post(f"/cases/{case_id}/appeals/{appeal_id}/resolve-authority")
    assert res.status_code == 200
    assert res.json()["status"] == "APPEAL_AUTHORITY_RESOLVED"
    
    # 3. Generate Draft
    with patch("agents.appeal_draft_generator.call_asi1") as mock_draft:
        mock_draft.return_value = "This is a First Appeal drafted text."
        res = client.post(f"/cases/{case_id}/appeals/{appeal_id}/generate-document")
        assert res.status_code == 200
        assert "First Appeal" in res.json()["content"]
        
    # 4. Quality Check
    res = client.post(f"/cases/{case_id}/appeals/{appeal_id}/quality-check")
    assert res.status_code == 200
    assert res.json()["status"] == "READY_TO_FILE"
    
    # 5. File Appeal
    payload = {
        "filing_date": str(date.today()),
        "filing_method": "ONLINE"
    }
    res = client.post(f"/cases/{case_id}/appeals/{appeal_id}/file", json=payload)
    assert res.status_code == 200
    
    # Check Case status
    case_res = client.get(f"/cases/{case_id}")
    assert case_res.json()["status"] == "APPEAL_AWAITING_RESPONSE"
    
    # Check Timeline (Deadline)
    timeline_res = client.get(f"/cases/{case_id}/timeline")
    assert timeline_res.status_code == 200
    deadlines = timeline_res.json()["deadlines"]
    assert len(deadlines) == 2 # 1 for RTI, 1 for Appeal
    appeal_dl = next(d for d in deadlines if d["deadline_type"] == "FIRST_APPEAL_RESPONSE")
    assert appeal_dl is not None
