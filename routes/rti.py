from fastapi import APIRouter, HTTPException
from models.schemas import RTIRequest, RTIResponse
from agents.intent_classifier import classify_intent
from agents.pio_resolver import resolve_pio
from agents.draft_generator import generate_draft, build_filing_instructions
from agents.quality_checker import check_quality
import random
import os

_GLOBAL_DEMO = os.getenv("DEMO_MODE", "false").lower() == "true"

router = APIRouter(prefix="/rti", tags=["RTI"])


def get_demo_response(request: RTIRequest) -> RTIResponse:
    """Generate instant demo response without calling AI APIs"""
    
    # Sample demo responses based on common scenarios
    demo_scenarios = {
        "ration": {
            "department": "Food and Civil Supplies Department",
            "ministry": "Ministry of Consumer Affairs, Food and Public Distribution",
            "information_needed": "Detailed reasons for ration card application rejection, name of the officer who rejected it, and complete file noting",
            "draft_english": """Date: [DD/MM/YYYY]

To,
The Public Information Officer,
Food and Civil Supplies Department,
[Your State] Government,
[Address]

Subject: Application under Right to Information Act, 2005

Respected Sir/Madam,

I am writing to request the following information under Section 6(1) of the Right to Information Act, 2005:

1. Complete details and specific reasons for the rejection of my ration card application filed on [DATE] with Application No. [APPLICATION_NUMBER].

2. Full name, designation, and office contact details of the officer who rejected my application.

3. Copy of the complete file noting and internal correspondence related to my application.

4. Copies of all documents, if any, that were found incomplete or incorrect in my application.

5. The standard operating procedure and checklist followed while processing ration card applications.

I am enclosing ₹10 as application fee via Indian Postal Order/Court Fee Stamp/DD No. [NUMBER].

This information is needed urgently as I am unable to access subsidized food grains and facing severe hardship.

If the information requested concerns the life and liberty of a person, I request you to provide the information within 48 hours as per Section 7(1) of the RTI Act.

Please provide the information within 30 days as mandated by the RTI Act, 2005.

Yours faithfully,

[YOUR FULL NAME]
[Complete Address]
[Mobile Number]
[Email ID]

Enclosures:
1. Fee payment proof (IPO/Stamp/DD)
2. Copy of rejected application (if available)""",
            "draft_hindi": """दिनांक: [DD/MM/YYYY]

सेवा में,
लोक सूचना अधिकारी,
खाद्य एवं नागरिक आपूर्ति विभाग,
[आपका राज्य] सरकार,
[पता]

विषय: सूचना के अधिकार अधिनियम, 2005 के तहत आवेदन

माननीय महोदय/महोदया,

मैं सूचना के अधिकार अधिनियम, 2005 की धारा 6(1) के तहत निम्नलिखित जानकारी का अनुरोध कर रहा/रही हूं:

1. [तारीख] को दाखिल किए गए मेरे राशन कार्ड आवेदन, आवेदन संख्या [आवेदन संख्या], के निरस्त होने के संपूर्ण विवरण और विशिष्ट कारण।

2. मेरे आवेदन को अस्वीकार करने वाले अधिकारी का पूरा नाम, पदनाम और कार्यालय संपर्क विवरण।

3. मेरे आवेदन से संबंधित संपूर्ण फाइल नोटिंग और आंतरिक पत्राचार की प्रति।

4. मेरे आवेदन में अधूरे या गलत पाए गए सभी दस्तावेजों की प्रतियां (यदि कोई हों)।

5. राशन कार्ड आवेदनों की प्रक्रिया के दौरान अपनाई जाने वाली मानक संचालन प्रक्रिया और चेकलिस्ट।

मैं आवेदन शुल्क के रूप में ₹10, भारतीय डाक आदेश/न्यायालय शुल्क टिकट/DD संख्या [संख्या] के माध्यम से संलग्न कर रहा/रही हूं।

यह जानकारी अत्यावश्यक है क्योंकि मैं सब्सिडी वाले खाद्यान्न प्राप्त करने में असमर्थ हूं और गंभीर कठिनाई का सामना कर रहा/रही हूं।

यदि अनुरोधित जानकारी किसी व्यक्ति के जीवन और स्वतंत्रता से संबंधित है, तो मैं आरटीआई अधिनियम की धारा 7(1) के अनुसार 48 घंटे के भीतर जानकारी प्रदान करने का अनुरोध करता/करती हूं।

कृपया आरटीआई अधिनियम, 2005 द्वारा अनिवार्य 30 दिनों के भीतर जानकारी प्रदान करें।

भवदीय,

[आपका पूरा नाम]
[पूरा पता]
[मोबाइल नंबर]
[ईमेल आईडी]

संलग्नक:
1. शुल्क भुगतान प्रमाण (IPO/स्टाम्प/DD)
2. अस्वीकृत आवेदन की प्रति (यदि उपलब्ध हो)"""
        },
        "passport": {
            "department": "Passport Seva Kendra",
            "ministry": "Ministry of External Affairs",
            "information_needed": "Status of passport application, reasons for delay, and expected timeline",
            "draft_english": """Date: [DD/MM/YYYY]

To,
The Public Information Officer,
Passport Seva Kendra,
[Your City],
Ministry of External Affairs,
Government of India

Subject: Application under Right to Information Act, 2005

Respected Sir/Madam,

I am writing to request the following information under Section 6(1) of the Right to Information Act, 2005:

1. Current status of my passport application filed on [DATE] with Application Reference No. [ARN].

2. Detailed reasons for the delay in processing my passport application beyond the standard timeline.

3. Name and designation of the officer currently assigned to my application.

4. Expected date of passport issuance or next action required from my end.

5. Details of any police verification status and report (if applicable).

6. Copy of all internal notes and correspondence related to my application.

I am enclosing ₹10 as application fee via Indian Postal Order/Court Fee Stamp/DD No. [NUMBER].

Please provide the information within 30 days as mandated by the RTI Act, 2005.

Yours faithfully,

[YOUR FULL NAME]
[Complete Address]
[Mobile Number]
[Email ID]

Enclosures:
1. Fee payment proof
2. Copy of passport application acknowledgment""",
            "draft_hindi": """दिनांक: [DD/MM/YYYY]

सेवा में,
लोक सूचना अधिकारी,
पासपोर्ट सेवा केंद्र,
[आपका शहर],
विदेश मंत्रालय,
भारत सरकार

विषय: सूचना के अधिकार अधिनियम, 2005 के तहत आवेदन

माननीय महोदय/महोदया,

मैं सूचना के अधिकार अधिनियम, 2005 की धारा 6(1) के तहत निम्नलिखित जानकारी का अनुरोध कर रहा/रही हूं:

1. [तारीख] को दाखिल किए गए मेरे पासपोर्ट आवेदन की वर्तमान स्थिति, आवेदन संदर्भ संख्या [ARN]।

2. मानक समयसीमा से अधिक समय तक मेरे पासपोर्ट आवेदन की प्रक्रिया में देरी के विस्तृत कारण।

3. मेरे आवेदन को वर्तमान में सौंपे गए अधिकारी का नाम और पदनाम।

4. पासपोर्ट जारी होने की अपेक्षित तिथि या मेरी ओर से आवश्यक अगली कार्रवाई।

5. पुलिस सत्यापन स्थिति और रिपोर्ट का विवरण (यदि लागू हो)।

6. मेरे आवेदन से संबंधित सभी आंतरिक नोट्स और पत्राचार की प्रति।

मैं आवेदन शुल्क के रूप में ₹10, भारतीय डाक आदेश/न्यायालय शुल्क टिकट/DD संख्या [संख्या] के माध्यम से संलग्न कर रहा/रही हूं।

कृपया आरटीआई अधिनियम, 2005 द्वारा अनिवार्य 30 दिनों के भीतर जानकारी प्रदान करें।

भवदीय,

[आपका पूरा नाम]
[पूरा पता]
[मोबाइल नंबर]
[ईमेल आईडी]

संलग्नक:
1. शुल्क भुगतान प्रमाण
2. पासपोर्ट आवेदन पावती की प्रति"""
        },
        "default": {
            "department": "General Administration Department",
            "ministry": "Ministry of Personnel, Public Grievances and Pensions",
            "information_needed": "Information about government service or application",
            "draft_english": """Date: [DD/MM/YYYY]

To,
The Public Information Officer,
[Department Name],
[Ministry Name],
Government of India/[State Name]

Subject: Application under Right to Information Act, 2005

Respected Sir/Madam,

I am writing to request the following information under Section 6(1) of the Right to Information Act, 2005:

1. Complete details and current status of my application/query regarding [your specific issue].

2. Name, designation, and contact details of the concerned officer handling this matter.

3. Copy of all relevant documents, file notings, and correspondence.

4. Expected timeline for resolution or next steps required.

I am enclosing ₹10 as application fee via Indian Postal Order/Court Fee Stamp/DD No. [NUMBER].

Please provide the information within 30 days as mandated by the RTI Act, 2005.

Yours faithfully,

[YOUR FULL NAME]
[Complete Address]
[Mobile Number]
[Email ID]

Enclosures:
1. Fee payment proof""",
            "draft_hindi": """दिनांक: [DD/MM/YYYY]

सेवा में,
लोक सूचना अधिकारी,
[विभाग का नाम],
[मंत्रालय का नाम],
भारत सरकार/[राज्य का नाम]

विषय: सूचना के अधिकार अधिनियम, 2005 के तहत आवेदन

माननीय महोदय/महोदया,

मैं सूचना के अधिकार अधिनियम, 2005 की धारा 6(1) के तहत निम्नलिखित जानकारी का अनुरोध कर रहा/रही हूं:

1. [आपके विशिष्ट मुद्दे] के संबंध में मेरे आवेदन/प्रश्न का संपूर्ण विवरण और वर्तमान स्थिति।

2. इस मामले को संभालने वाले संबंधित अधिकारी का नाम, पदनाम और संपर्क विवरण।

3. सभी प्रासंगिक दस्तावेजों, फाइल नोटिंग और पत्राचार की प्रति।

4. समाधान के लिए अपेक्षित समयसीमा या आवश्यक अगले कदम।

मैं आवेदन शुल्क के रूप में ₹10, भारतीय डाक आदेश/न्यायालय शुल्क टिकट/DD संख्या [संख्या] के माध्यम से संलग्न कर रहा/रही हूं।

कृपया आरटीआई अधिनियम, 2005 द्वारा अनिवार्य 30 दिनों के भीतर जानकारी प्रदान करें।

भवदीय,

[आपका पूरा नाम]
[पूरा पता]
[मोबाइल नंबर]
[ईमेल आईडी]

संलग्नक:
1. शुल्क भुगतान प्रमाण"""
        }
    }
    
    # Detect scenario from description
    desc_lower = request.description.lower()
    scenario_key = "default"
    
    if any(word in desc_lower for word in ["ration", "राशन", "food", "card"]):
        scenario_key = "ration"
    elif any(word in desc_lower for word in ["passport", "पासपोर्ट"]):
        scenario_key = "passport"
    
    scenario = demo_scenarios[scenario_key]
    draft = scenario[f"draft_{request.language}"] if request.language == "hindi" else scenario["draft_english"]
    
    # Determine state and government level
    gov_level = "state" if request.state else "central"
    state_name = request.state or "Central Government"
    
    return RTIResponse(
        draft=draft,
        filing_instructions=f"""📋 **Filing Instructions** (DEMO MODE)

**Step 1: Prepare Documents**
- Print the RTI draft above on plain paper
- Fill in all placeholder fields marked with [SQUARE BRACKETS]
- Sign the application

**Step 2: Payment**
- Fee: ₹10 (₹20 for Gujarat)
- Payment Mode: Indian Postal Order (IPO) or Court Fee Stamp
- BPL cardholders: Attach BPL certificate copy for FREE filing

**Step 3: File the Application**
- Online: Visit rtionline.gov.in and upload scanned copy
- Offline: Send by Speed Post to the PIO address mentioned in the draft
- Keep acknowledgment/tracking number for reference

**Timeline:**
- Response expected within 30 days from filing date
- For life-threatening matters: 48 hours (mention this clearly)

**If no response:**
- File First Appeal after 30 days to the Appellate Authority
- Use /appeal command in this bot to generate appeal letter

⚠️ This is a DEMO response. Enable real mode by setting demo_mode=false.""",
        department=scenario["department"],
        ministry=scenario["ministry"],
        government_level=gov_level,
        information_needed=scenario["information_needed"],
        urgency="routine",
        pio_details={
            "pio_designation": "Public Information Officer",
            "appellate_authority_designation": "First Appellate Authority",
            "address_format": f"{scenario['department']}, {scenario['ministry']}, {state_name}",
            "filing_fee": "₹10",
            "fee_payment_modes": ["Indian Postal Order", "Court Fee Stamp", "Demand Draft"],
            "response_timeline_days": 30,
            "life_threatening_timeline_days": 2,
            "online_portal": "https://rtionline.gov.in",
            "additional_notes": "This is a DEMO response generated instantly without AI processing."
        },
        quality_score=85,
        is_valid=True,
        warnings=["⚠️ DEMO MODE: This is a sample response for demonstration purposes."],
        suggestions=[
            "Fill in all placeholder fields like [DATE], [APPLICATION_NUMBER], etc.",
            "Attach required documents and fee payment proof",
            "Keep a copy of the filed RTI for your records"
        ],
        exempt_risk="low",
        estimated_success_probability="high",
        confidence=1.0
    )


@router.post(
    "/generate",
    response_model=RTIResponse,
    summary="Generate RTI Application",
    description="""
    **4-Layer AI Pipeline:**

    1. **Intent Classifier** — Identifies the correct department, ministry, and urgency
    2. **PIO Resolver** — Finds the correct Public Information Officer details
    3. **Draft Generator** — Creates a legally correct RTI application
    4. **Quality Checker** — Reviews for completeness, specificity, and exemption risks

    Returns a complete, ready-to-file RTI application with filing instructions.
    
    **Demo Mode:** Set `demo_mode=true` for instant sample responses without API calls (useful for demos/testing).
    """,
)
async def generate_rti(request: RTIRequest):
    try:
        # ── DEMO MODE: Return instant sample response ─────────────
        # Respect global DEMO_MODE env var OR per-request flag
        if _GLOBAL_DEMO or request.demo_mode:
            return get_demo_response(request)
        # ── Layer 1: Classify intent ──────────────────────────────────
        intent = classify_intent(request.description)

        if intent["confidence"] < 0.4:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Could not identify the correct government department with sufficient confidence "
                    f"(confidence: {intent['confidence']:.0%}). "
                    "Please provide more details about which government body or service your query relates to."
                ),
            )

        # ── Layer 2: Resolve PIO ──────────────────────────────────────
        pio_info = resolve_pio(
            department=intent["department"],
            ministry=intent["ministry"],
            government_level=intent.get("government_level", "central"),
            state_name=intent.get("state_name") or request.state,
        )

        # ── Layer 3: Generate draft ───────────────────────────────────
        draft = generate_draft(
            intent=intent,
            pio_info=pio_info,
            language=request.language,
        )

        # ── Layer 4: Quality check ────────────────────────────────────
        quality = check_quality(draft)

        # Build filing instructions
        filing_instructions = build_filing_instructions(pio_info, intent)

        return RTIResponse(
            draft=draft,
            filing_instructions=filing_instructions,
            department=intent["department"],
            ministry=intent["ministry"],
            government_level=intent.get("government_level", "central"),
            information_needed=intent["information_needed"],
            urgency=intent["urgency"],
            pio_details=pio_info,
            quality_score=quality["score"],
            is_valid=quality["is_valid"],
            warnings=quality.get("issues", []),
            suggestions=quality.get("suggestions", []),
            exempt_risk=quality.get("exempt_risk", "low"),
            estimated_success_probability=quality.get("estimated_success_probability", "medium"),
            confidence=intent["confidence"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")
