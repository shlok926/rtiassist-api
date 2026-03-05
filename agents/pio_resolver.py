import json
from utils.asi1_client import call_asi1
from prompts.system_prompts import PIO_RESOLVER


def resolve_pio(department: str, ministry: str, government_level: str = "central", state_name: str = None) -> dict:
    """
    Layer 2: Resolve the correct Public Information Officer details.
    Identifies PIO designation, appellate authority, address, fee, and filing portal.

    Args:
        department: Government department name
        ministry: Government ministry name
        government_level: 'central' or 'state'
        state_name: State name if state-level RTI

    Returns:
        dict with PIO designation, appellate authority, address format, fee, portal, etc.
    """
    user_message = (
        f"Department: {department}\n"
        f"Ministry: {ministry}\n"
        f"Government Level: {government_level}\n"
        f"State: {state_name or 'N/A (Central Government)'}"
    )

    raw = call_asi1(
        system_prompt=PIO_RESOLVER,
        user_message=user_message,
        temperature=0.2,
        max_tokens=500,
    )

    try:
        clean = raw.strip().strip("```json").strip("```").strip()
        result = json.loads(clean)
    except json.JSONDecodeError:
        # Safe fallback defaults
        result = {
            "pio_designation": f"Public Information Officer, {department}",
            "appellate_authority_designation": f"First Appellate Authority, {ministry}",
            "address_format": f"The PIO, {department}, {ministry}, Government of India, New Delhi",
            "filing_fee": "Rs. 10 (Central Government)",
            "fee_payment_modes": ["IPO", "DD", "Court Fee Stamp"],
            "response_timeline_days": 30,
            "life_threatening_timeline_days": 48,
            "online_portal": "https://rtionline.gov.in",
            "additional_notes": "File online at rtionline.gov.in for faster processing.",
        }

    return result
