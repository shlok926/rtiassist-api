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

client = TestClient(app, raise_server_exceptions=True)


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

def mock_pio(department, ministry, government_level, state_name):
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
    def test_legacy_endpoint_deprecated(self):
        """Legacy /rti/generate should return 410 Gone"""
        response = client.post("/rti/generate", json={
            "description": "My ration card application was rejected 3 months ago and I want to know the exact reason and which officer rejected it.",
            "language": "english",
            "state": "Maharashtra"
        })
        assert response.status_code == 410
        assert "deprecated" in response.json()["detail"].lower()
