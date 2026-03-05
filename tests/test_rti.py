"""
RTIAssist API — Test Cases
Run with: pytest tests/test_rti.py -v
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


# ── Mock ASI-1 response factory ───────────────────────────────────────────────

def mock_intent(description):
    return {
        "information_needed": "Reason for ration card rejection",
        "department": "Food and Civil Supplies Department",
        "ministry": "Ministry of Consumer Affairs, Food and Public Distribution",
        "government_level": "state",
        "state_name": "Maharashtra",
        "rti_section": "Section 6(1) of RTI Act 2005",
        "urgency": "urgent",
        "urgency_reason": "Affects food security",
        "confidence": 0.92,
    }

def mock_pio(dept, ministry, govt_level, state_name):
    return {
        "pio_designation": "Public Information Officer, Food and Civil Supplies",
        "appellate_authority_designation": "Deputy Director, Food and Civil Supplies",
        "address_format": "The PIO, Food and Civil Supplies Dept, Mantralaya, Mumbai - 400032",
        "filing_fee": "Rs. 10",
        "fee_payment_modes": ["IPO", "Court Fee Stamp", "Online Portal"],
        "response_timeline_days": 30,
        "life_threatening_timeline_days": 48,
        "online_portal": "https://rtionline.gov.in",
        "additional_notes": "State RTI portal also available.",
    }

def mock_draft(intent, pio_info, language):
    return """Date: [DATE]

To,
The Public Information Officer,
Food and Civil Supplies Department,
[ADDRESS]

Subject: Application under Section 6(1) of the Right to Information Act, 2005

Respected Sir/Madam,

I, [APPLICANT_NAME], son/daughter/wife of [FATHER_HUSBAND_NAME], residing at [ADDRESS_LINE_1], [CITY_PIN], hereby request the following information under Section 6(1) of the Right to Information Act, 2005:

1. The specific reason(s) for rejection of my ration card application.
2. The name and designation of the officer who rejected my application.
3. A copy of the rejection order/letter with all relevant notings.
4. The date on which the rejection decision was made.

I am enclosing a fee of Rs. [FEE_AMOUNT] via [PAYMENT_MODE] (Reference: [PAYMENT_REFERENCE]).

If I am a BPL cardholder, I am exempt from paying the fee and have enclosed proof.

Yours faithfully,
[APPLICANT_NAME]
Phone: [PHONE_NUMBER]
Email: [EMAIL_ADDRESS]
Date: [DATE]"""

def mock_quality(draft):
    return {
        "is_valid": True,
        "score": 88,
        "issues": [],
        "suggestions": ["Consider adding the application number if available."],
        "exempt_risk": "none",
        "exempt_risk_reason": "",
        "estimated_success_probability": "high",
        "reviewer_notes": "Well-drafted application. Ready to file.",
    }


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestHealthEndpoints:
    def test_root_returns_ok(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "✅ RTIAssist API is running"

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestRTIGenerate:
    @patch("routes.rti.classify_intent", side_effect=mock_intent)
    @patch("routes.rti.resolve_pio", side_effect=mock_pio)
    @patch("routes.rti.generate_draft", side_effect=mock_draft)
    @patch("routes.rti.check_quality", side_effect=mock_quality)
    def test_ration_card_rejection(self, *mocks):
        """Scenario 1: Ration card rejection reason"""
        response = client.post("/rti/generate", json={
            "description": "My ration card application was rejected 3 months ago and I want to know the exact reason and which officer rejected it.",
            "language": "english",
            "state": "Maharashtra"
        })
        assert response.status_code == 200
        data = response.json()
        assert "draft" in data
        assert "[APPLICANT_NAME]" in data["draft"]
        assert data["quality_score"] >= 70
        assert data["is_valid"] is True
        assert data["confidence"] > 0.5

    def test_missing_description(self):
        """Should fail with 422 for missing required field"""
        response = client.post("/rti/generate", json={
            "language": "english"
        })
        assert response.status_code == 422

    def test_description_too_short(self):
        """Should fail with 422 for description under 20 chars"""
        response = client.post("/rti/generate", json={
            "description": "RTI about PAN",
        })
        assert response.status_code == 422

    @patch("routes.rti.classify_intent", side_effect=mock_intent)
    @patch("routes.rti.resolve_pio", side_effect=mock_pio)
    @patch("routes.rti.generate_draft", side_effect=mock_draft)
    @patch("routes.rti.check_quality", side_effect=mock_quality)
    def test_hindi_language_flag(self, *mocks):
        """Scenario 2: Hindi language request"""
        response = client.post("/rti/generate", json={
            "description": "I want to know why my land mutation application is pending for 6 months in the revenue department.",
            "language": "hindi",
        })
        assert response.status_code == 200

    @patch("routes.rti.classify_intent", side_effect=mock_intent)
    @patch("routes.rti.resolve_pio", side_effect=mock_pio)
    @patch("routes.rti.generate_draft", side_effect=mock_draft)
    @patch("routes.rti.check_quality", side_effect=mock_quality)
    def test_response_structure_completeness(self, *mocks):
        """All required fields must be present in response"""
        response = client.post("/rti/generate", json={
            "description": "I want to know the salary slips of all grade A officers in my district for last 3 months.",
        })
        assert response.status_code == 200
        data = response.json()

        required_fields = [
            "draft", "filing_instructions", "department", "ministry",
            "government_level", "information_needed", "urgency",
            "pio_details", "quality_score", "is_valid", "warnings",
            "suggestions", "exempt_risk", "estimated_success_probability", "confidence"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
