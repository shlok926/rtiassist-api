import pytest
import json
import os
import io
from unittest.mock import patch
from fastapi.testclient import TestClient
from datetime import date, datetime, timezone

from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from fpdf import FPDF

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rtiassist_responses.db"

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

def setup_filed_case():
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
    
    return case_id

def create_fake_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Your complaint has been forwarded. No action taken yet.", ln=True, align="C")
    return pdf.output(dest="S") # Returns bytearray

def test_upload_and_analyze_response():
    case_id = setup_filed_case()
    
    pdf_bytes = bytes(create_fake_pdf(), "latin1")
    
    # Mock the LLM Response Analysis
    mock_llm_response = json.dumps({
        "status": "PARTIALLY_ANSWERED",
        "answered": ["Complaint forwarded"],
        "not_answered": ["Action taken"],
        "recommended_action": "FIRST_APPEAL",
        "request_mapping": []
    })
    
    with patch("agents.response_analyzer.call_asi1") as mock_llm:
        mock_llm.return_value = mock_llm_response
        
        # We need to simulate uploading a file using FastAPI TestClient
        res = client.post(
            f"/cases/{case_id}/responses",
            files={"file": ("response.pdf", pdf_bytes, "application/pdf")}
        )
        
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PARTIALLY_ANSWERED"
    assert data["recommended_action"] == "FIRST_APPEAL"
    assert "Complaint forwarded" in data["answered"]
    
    # Verify State Transition
    case_res = client.get(f"/cases/{case_id}")
    assert case_res.json()["status"] == "ANALYSIS_READY"
    
def test_upload_invalid_file_type():
    case_id = setup_filed_case()
    
    # Use text file instead of PDF
    res = client.post(
        f"/cases/{case_id}/responses",
        files={"file": ("response.txt", b"some text", "text/plain")}
    )
    
    assert res.status_code == 400
    assert "Only PDF files are allowed" in res.json()["detail"]
    
def test_invalid_case_state_for_upload():
    # Case in UNDERSTANDING state
    res = client.post("/cases", json={"problem_description": "Test"})
    case_id = res.json()["id"]
    
    pdf_bytes = bytes(create_fake_pdf(), "latin1")
    res = client.post(
        f"/cases/{case_id}/responses",
        files={"file": ("response.pdf", pdf_bytes, "application/pdf")}
    )
    
    assert res.status_code == 400
    assert "not awaiting a response" in res.json()["detail"]
