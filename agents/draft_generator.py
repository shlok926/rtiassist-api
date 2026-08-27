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
    LANGUAGE_MAP = {
        "hindi":     "Hindi (Devanagari script — हिन्दी)",
        "marathi":   "Marathi (Devanagari script — मराठी)",
        "tamil":     "Tamil (Tamil script — தமிழ்)",
        "telugu":    "Telugu (Telugu script — తెలుగు)",
        "kannada":   "Kannada (Kannada script — ಕನ್ನಡ)",
        "bengali":   "Bengali (Bengali script — বাংলা)",
        "gujarati":  "Gujarati (Gujarati script — ગુજરાતી)",
        "punjabi":   "Punjabi (Gurmukhi script — ਪੰਜਾਬੀ)",
        "malayalam": "Malayalam (Malayalam script — മലയാളം)",
        "odia":      "Odia (Odia script — ଓଡ଼ିଆ)",
        "english":   "formal English",
    }
    lang_key = language.lower().strip()
    lang_name = LANGUAGE_MAP.get(lang_key, "formal English")
    language_instruction = (
        f"IMPORTANT: You MUST write the ENTIRE application in {lang_name}. "
        f"Every word — including the heading, addressee block, subject line, body, "
        f"and closing — must be in {lang_name}. Do NOT use English unless the language itself is English."
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
        temperature=0.3,
        max_tokens=2500,
    )

    return draft

def generate_case_draft(problem_description: str, action: str, authority_context: dict, language: str = "english") -> str:
    """
    Phase 5: Case-Based Document Generation.
    Uses problem description and verified authority context to draft the document.
    """
    LANGUAGE_MAP = {
        "hindi":     "Hindi (Devanagari script — हिन्दी)",
        "marathi":   "Marathi (Devanagari script — मराठी)",
        "tamil":     "Tamil (Tamil script — தமிழ்)",
        "telugu":    "Telugu (Telugu script — తెలుగు)",
        "kannada":   "Kannada (Kannada script — ಕನ್ನಡ)",
        "bengali":   "Bengali (Bengali script — বাংলা)",
        "gujarati":  "Gujarati (Gujarati script — ગુજરાતી)",
        "punjabi":   "Punjabi (Gurmukhi script — ਪੰਜਾਬੀ)",
        "malayalam": "Malayalam (Malayalam script — മലയാളം)",
        "odia":      "Odia (Odia script — ଓଡ଼ିଆ)",
        "english":   "formal English",
    }
    lang_key = language.lower().strip()
    lang_name = LANGUAGE_MAP.get(lang_key, "formal English")
    language_instruction = (
        f"IMPORTANT: You MUST write the ENTIRE application in {lang_name}. "
        f"Every word — including the heading, addressee block, subject line, body, "
        f"and closing — must be in {lang_name}. Do NOT use English unless the language itself is English."
    )

    user_message = f"""
{language_instruction}

Citizen Objective/Problem: {problem_description}
Document Type: {action}

Addressee details (From Verified Source):
- PIO Designation: {authority_context.get('pio_designation', 'Public Information Officer')}
- Department: {authority_context.get('department')}
- Ministry: {authority_context.get('ministry', '')}
- Address: {authority_context.get('address', '')}

Filing details:
- Filing Fee: {authority_context.get('filing_fee', '')}
- Accepted Payment Modes: {authority_context.get('payment_methods', '')}

Draft a complete, ready-to-file {action} application now. Ensure it matches the requested language perfectly.
"""

    draft = call_asi1(
        system_prompt=DRAFT_GENERATOR,
        user_message=user_message,
        temperature=0.3,
        max_tokens=2500,
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
