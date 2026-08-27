import pytest
import json
import os
import tempfile
from fpdf import FPDF
from unittest.mock import patch
from fastapi.testclient import TestClient
from models.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models.orm.case import Case
from models.orm.document import Document
from datetime import date

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_response_mapping.db"

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

def create_fake_pdf(text="Test"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=text, ln=True, align="C")
    fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    pdf.output(temp_path)
    return temp_path

def mock_call_asi1_response(*args, **kwargs):
    return json.dumps({
        "status": "PARTIALLY_ANSWERED",
        "answered": ["Question 1"],
        "not_answered": ["Question 2"],
        "recommended_action": "FIRST_APPEAL",
        "request_mapping": [
            {
                "request_text": "Provide copy of work order.",
                "status": "ANSWERED",
                "evidence_excerpt": "Enclosed on page 2",
                "page_number": 2,
                "is_ocr_derived": False
            },
            {
                "request_text": "Provide file notings.",
                "status": "NOT_ANSWERED",
                "evidence_excerpt": None,
                "page_number": None,
                "is_ocr_derived": False
            }
        ],
        "review_required": False
    })

def mock_call_asi1_ocr_warning(*args, **kwargs):
    return json.dumps({
        "status": "NOT_ANSWERED",
        "answered": [],
        "not_answered": ["All"],
        "recommended_action": "NEEDS_HUMAN_REVIEW",
        "request_mapping": [
            {
                "request_text": "Copy of file noting",
                "status": "NOT_ANSWERED",
                "evidence_excerpt": "Thjls dkls jlksdjf",
                "page_number": 1,
                "is_ocr_derived": True
            }
        ],
        "review_required": True
    })

def test_response_mapping():
    # Use endpoints to bypass FK issue
    res = client.post("/cases", json={"problem_description": "I want road repair info."})
    case_id = res.json()["id"]
    
    # Mock LLM to skip steps
    with patch("agents.action_recommender.call_asi1") as mock_asi1:
        mock_asi1.return_value = json.dumps({
            "recommended_action": "RTI", "confidence": 0.9, "objective": "", "reasoning": [],
            "alternative_actions": [], "missing_information": [], "required_documents": [],
            "urgency": "NORMAL", "supported": True, "warnings": []
        })
        client.post(f"/cases/{case_id}/recommend-action")
        client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
        
    # We need a Document for RTI
    db = TestingSessionLocal()
    doc = Document(case_id=case_id, document_type="RTI", status="READY_TO_FILE", content="1. Provide copy of work order.\n2. Provide file notings.", language="english", version="v1")
    db.add(doc)
    case = db.query(Case).filter(Case.id == case_id).first()
    case.status = "AWAITING_RESPONSE"
    db.commit()
    db.close()
    
    # Upload Response
    temp_path = create_fake_pdf("Government response text")
    with patch("services.response_service.analyze_response") as mock_analyze, \
         patch("services.ocr_service.OCRService.extract_text") as mock_ocr:
        mock_analyze.return_value = json.loads(mock_call_asi1_response())
        mock_ocr.return_value = {"text": "Government response text", "method": "native", "ocr_used": False, "page_count": 1}
        
        with open(temp_path, "rb") as f:
            res = client.post(f"/cases/{case_id}/responses", files={"file": ("resp.pdf", f, "application/pdf")})
            
    os.remove(temp_path)
    
    if res.status_code != 200:
        print("ERROR:", res.json())
        
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PARTIALLY_ANSWERED"
    assert data["recommended_action"] == "FIRST_APPEAL"
    
    mapping = data["request_mapping"]
    assert len(mapping) == 2
    assert mapping[0]["status"] == "ANSWERED"
    assert mapping[1]["status"] == "NOT_ANSWERED"

def test_ocr_warning_review_required():
    res = client.post("/cases", json={"problem_description": "I want info."})
    case_id = res.json()["id"]
    
    with patch("agents.action_recommender.call_asi1") as mock_asi1:
        mock_asi1.return_value = json.dumps({
            "recommended_action": "RTI", "confidence": 0.9, "objective": "", "reasoning": [],
            "alternative_actions": [], "missing_information": [], "required_documents": [],
            "urgency": "NORMAL", "supported": True, "warnings": []
        })
        client.post(f"/cases/{case_id}/recommend-action")
        client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"})
    
    db = TestingSessionLocal()
    doc = Document(case_id=case_id, document_type="RTI", status="READY_TO_FILE", content="1. Copy of file noting", language="english", version="v1")
    db.add(doc)
    case = db.query(Case).filter(Case.id == case_id).first()
    case.status = "AWAITING_RESPONSE"
    db.commit()
    db.close()
    
    temp_path = create_fake_pdf("Thjls dkls jlksdjf")
    with patch("services.response_service.analyze_response") as mock_analyze, \
         patch("services.ocr_service.OCRService.extract_text") as mock_ocr:
        mock_analyze.return_value = json.loads(mock_call_asi1_ocr_warning())
        mock_ocr.return_value = {"text": "Thjls dkls jlksdjf", "method": "ocr", "ocr_used": True, "page_count": 1}
        
        with open(temp_path, "rb") as f:
            res = client.post(f"/cases/{case_id}/responses", files={"file": ("resp.pdf", f, "application/pdf")})
            
    os.remove(temp_path)
    
    if res.status_code != 200:
        print("ERROR:", res.json())
        
    assert res.status_code == 200
    data = res.json()
    assert data["recommended_action"] == "NEEDS_HUMAN_REVIEW"
    assert data["request_mapping"][0]["is_ocr_derived"] is True
