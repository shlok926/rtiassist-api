from utils.asi1_client import call_asi1
from prompts.system_prompts import DRAFT_GENERATOR


def generate_draft(intent: dict, pio_info: dict, language: str = "english") -> str:
    """
    Layer 3: Generate a complete, formal RTI application draft.
    Uses intent classification and PIO details to produce a legally correct application.

    Args:
        intent: Output from classify_intent()
        pio_info: Output from resolve_pio()
        language: 'english' or 'hindi'

    Returns:
        Full RTI application text as a string (with placeholder fields)
    """
    language_instruction = (
        "Draft the application in Hindi (Devanagari script)."
        if language.lower() == "hindi"
        else "Draft the application in formal English."
    )

    user_message = f"""
{language_instruction}

Information to seek: {intent['information_needed']}

Addressee details:
- PIO Designation: {pio_info['pio_designation']}
- Department: {intent['department']}
- Ministry: {intent['ministry']}
- Address Format: {pio_info['address_format']}

Filing details:
- Filing Fee: {pio_info['filing_fee']}
- Accepted Payment Modes: {', '.join(pio_info['fee_payment_modes'])}
- RTI Section: {intent['rti_section']}
- Urgency: {intent['urgency']}

Draft a complete, ready-to-file RTI application now.
"""

    draft = call_asi1(
        system_prompt=DRAFT_GENERATOR,
        user_message=user_message,
        temperature=0.4,  # Slightly higher for natural legal language variation
        max_tokens=1200,
    )

    return draft


def build_filing_instructions(pio_info: dict, intent: dict) -> str:
    """
    Generate plain-language filing instructions for the citizen.
    """
    urgency = intent.get("urgency", "routine")
    timeline = (
        pio_info.get("life_threatening_timeline_days", 48)
        if urgency == "life_threatening"
        else pio_info.get("response_timeline_days", 30)
    )

    portal = pio_info.get("online_portal")
    portal_line = (
        f"You can file online at: {portal}"
        if portal
        else "File physically by post or in person at the department."
    )

    instructions = f"""
HOW TO FILE YOUR RTI APPLICATION:

1. FILL IN PLACEHOLDERS
   Replace all [SQUARE_BRACKET] fields with your actual details before filing.

2. PAYMENT
   Pay {pio_info['filing_fee']} via {' or '.join(pio_info['fee_payment_modes'])}.
   BPL (Below Poverty Line) applicants are exempt — attach BPL card copy.

3. FILE THE APPLICATION
   {portal_line}
   Alternatively, send by registered post to the PIO address mentioned in the application.

4. KEEP A COPY
   Always keep a signed copy of your application and payment receipt.

5. EXPECTED RESPONSE TIME
   The PIO must respond within {timeline} {'hours' if urgency == 'life_threatening' else 'days'}.
   {'⚠️ This is a LIFE-THREATENING urgency request — response is legally required within 48 hours.' if urgency == 'life_threatening' else ''}

6. IF NO RESPONSE
   File a First Appeal with: {pio_info['appellate_authority_designation']}
   First appeal must be filed within 30 days of deadline expiry.
   Second appeal goes to the Central/State Information Commission.
""".strip()

    return instructions
