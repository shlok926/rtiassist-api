import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import date
from sqlalchemy.orm import Session

from main import app
from models.database import Base, engine, get_db
from models.schemas import AuthorityResolution
from utils.security import get_password_hash
from models.orm.user import User

client = TestClient(app)

# Helper function to create users and get auth headers
def create_test_user(db: Session, email: str = "test@example.com") -> str:
    # Attempt to register first
    client.post("/auth/register", json={"email": email, "password": "password123"})
    
    response = client.post(
        "/auth/login",
        json={"email": email, "password": "password123"}
    )
    return response.json()["access_token"]

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_header_a():
    db = next(get_db())
    token = create_test_user(db, "userA@example.com")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_header_b():
    db = next(get_db())
    token = create_test_user(db, "userB@example.com")
    return {"Authorization": f"Bearer {token}"}

@patch("services.case_service.action_recommender.recommend_action")
@patch("services.case_service.authority_service.resolve_authority_for_case")
@patch("services.document_service.draft_generator.generate_case_draft")
@patch("services.document_service.quality_checker.check_quality")
@patch("services.document_service.authority_repository.get_by_id")
def test_full_case_lifecycle(mock_get_authority, mock_quality, mock_draft, mock_authority, mock_recommend, auth_header_a):
    """End-to-End test of the full citizen lifecycle."""
    # Mocks
    mock_recommend.return_value = {
        "recommended_action": "RTI",
        "confidence": 0.9,
        "objective": "Get information",
        "reasoning": [],
        "alternative_actions": [],
        "missing_information": [],
        "required_documents": [],
        "urgency": "normal",
        "supported": True,
        "warnings": []
    }
    
    mock_authority.return_value = AuthorityResolution(
        match_status="MATCHED",
        authority_id="test_auth_id",
        confidence="HIGH",
        reason="Exact match"
    )
    
    from datetime import datetime, timezone
    mock_get_authority.return_value = MagicMock(
        verification_status="VERIFIED",
        active=True,
        department="Test Dept",
        ministry="Test Min",
        government_level="Central",
        state=None,
        district=None,
        pio_designation="PIO",
        appellate_authority_designation="FAA",
        address="123 Test St",
        filing_fee="10",
        payment_methods="Cash",
        online_portal=None,
        source_url="http://example.com",
        last_verified=datetime.now(timezone.utc)
    )
    
    mock_draft.return_value = "This is a generated RTI draft."
    
    mock_quality.return_value = {
        "is_valid": True,
        "score": 95,
        "issues": [],
        "suggestions": []
    }
    
    # 1. CREATE CASE
    response = client.post("/cases", json={"problem_description": "Water supply issue"}, headers=auth_header_a)
    assert response.status_code == 200
    case_id = response.json()["id"]
    
    # 2. RECOMMEND ACTION
    response = client.post(f"/cases/{case_id}/recommend-action", headers=auth_header_a)
    assert response.status_code == 200
    
    # 3. CONFIRM ACTION
    response = client.post(f"/cases/{case_id}/confirm-action", json={"action": "RTI"}, headers=auth_header_a)
    assert response.status_code == 200
    assert response.json()["status"] == "ACTION_CONFIRMED"
    
    # 4. RESOLVE AUTHORITY
    response = client.post(f"/cases/{case_id}/resolve-authority", headers=auth_header_a)
    assert response.status_code == 200
    
    # 5. GENERATE DOCUMENT
    response = client.post(f"/cases/{case_id}/generate-document", json={"language": "english"}, headers=auth_header_a)
    assert response.status_code == 200
    doc_id = response.json()["id"]
    
    # Verify status changed to READY_TO_FILE
    case_response = client.get(f"/cases/{case_id}", headers=auth_header_a)
    assert case_response.json()["status"] == "READY_TO_FILE"
    
    # 6. FILING
    response = client.post(f"/cases/{case_id}/file", json={
        "filing_date": date.today().isoformat(),
        "filing_method": "ONLINE",
        "reference_number": "RTI/12345"
    }, headers=auth_header_a)
    assert response.status_code == 200
    
    # Verify status changed to AWAITING_RESPONSE
    case_response = client.get(f"/cases/{case_id}", headers=auth_header_a)
    assert case_response.json()["status"] == "AWAITING_RESPONSE"

def test_cross_tenant_idor(auth_header_a, auth_header_b):
    """Test that User B cannot access User A's case resources."""
    # User A creates a case
    response = client.post("/cases", json={"problem_description": "IDOR Test"}, headers=auth_header_a)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    case_id = response.json()["id"]
    
    # User B attempts to access User A's case
    assert client.get(f"/cases/{case_id}", headers=auth_header_b).status_code == 404
    assert client.patch(f"/cases/{case_id}", json={"status": "CLOSED"}, headers=auth_header_b).status_code == 404
    assert client.post(f"/cases/{case_id}/recommend-action", headers=auth_header_b).status_code == 404
    assert client.get(f"/cases/{case_id}/timeline", headers=auth_header_b).status_code == 404
