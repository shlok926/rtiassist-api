from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, date


class RTIRequest(BaseModel):
    description: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        description="Plain-language description of what government information you need.",
        example="My ration card application was rejected 3 months ago and I want to know the exact reason and the officer who rejected it.",
    )
    language: str = Field(
        default="english",
        description="Language for the RTI draft: english, hindi, marathi, tamil, telugu, kannada, bengali, gujarati, punjabi, malayalam, odia",
    )
    state: Optional[str] = Field(
        default=None,
        description="State name if filing a state-level RTI. Leave blank for Central Government.",
        example="Maharashtra",
    )
    demo_mode: Optional[bool] = Field(
        default=None,
        description="Set true for instant demo response, false to force real AI, omit to use server default.",
    )


class PIORTIDetails(BaseModel):
    pio_designation: str
    appellate_authority_designation: str
    address_format: str
    filing_fee: str
    fee_payment_modes: List[str]
    response_timeline_days: int
    life_threatening_timeline_days: int
    online_portal: Optional[str]
    additional_notes: Optional[str]


class RTIResponse(BaseModel):
    # Core output
    draft: str = Field(..., description="Complete RTI application text ready to fill and file")
    filing_instructions: str = Field(..., description="Step-by-step plain English filing guide")

    # Classification results
    department: str
    ministry: str
    government_level: str
    information_needed: str
    urgency: str

    # PIO details
    pio_details: dict

    # Quality assessment
    quality_score: int = Field(..., ge=0, le=100, description="Quality score out of 100")
    is_valid: bool
    warnings: List[str]
    suggestions: List[str]
    exempt_risk: str = Field(..., description="Risk of exemption under Section 8: none/low/medium/high")
    estimated_success_probability: str

    # Meta
    confidence: float = Field(..., description="AI confidence in department classification (0.0 to 1.0)")


class HealthResponse(BaseModel):
    status: str
    version: str
    model: str
    endpoints: List[str]

# --- Phase 2 Schemas ---
from datetime import datetime
from pydantic import ConfigDict

class CaseEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    event_type: str
    description: str
    created_at: datetime
    metadata_json: Optional[str] = None

class DocumentMetadataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    document_type: str
    title: Optional[str] = None
    created_at: datetime
    mime_type: Optional[str] = None

class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    status: str
    problem_description: str
    title: Optional[str] = None
    priority: Optional[str] = None
    recommended_action: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    events: Optional[List[CaseEventResponse]] = None
    documents: Optional[List[DocumentMetadataResponse]] = None
    
    # Phase 6 Summary Fields
    filing_date: Optional[date] = None
    next_deadline: Optional[date] = None
    remaining_days: Optional[int] = None
    overdue: Optional[bool] = None
    
    # Phase 13: Case Intelligence
    case_objective: Optional[str] = None
    extracted_facts: Optional[str] = None
    facts_confirmed: Optional[str] = None
    next_action_recommendation: Optional[str] = None
    response_analyses: Optional[List['ResponseAnalysisResponse']] = None
    appeals: Optional[List['AppealResponse']] = None

class CaseListResponse(BaseModel):
    cases: List[CaseResponse]
    total: int

class CaseCreate(BaseModel):
    problem_description: str = Field(..., description="Description of the citizen's problem")
    title: Optional[str] = Field(None, description="Optional title for the case")

class CaseUpdate(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None
    priority: Optional[str] = None
    recommended_action: Optional[str] = None
    case_objective: Optional[str] = None
    extracted_facts: Optional[str] = None
    facts_confirmed: Optional[str] = None

class TrackerImport(BaseModel):
    id: str
    date: str
    department: str
    description: str
    status: str

# --- Phase 3 Schemas ---

class ActionRecommendation(BaseModel):
    recommended_action: str
    confidence: float
    objective: str
    reasoning: List[str]
    alternative_actions: List[str]
    missing_information: List[str]
    required_documents: List[str]
    urgency: str
    supported: bool
    warnings: List[str]
    extracted_facts: Optional[dict] = None

class ActionConfirmation(BaseModel):
    action: str

# --- Phase 4 Schemas ---

class AuthoritySource(BaseModel):
    title: Optional[str] = None
    url: str

class AuthorityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    department: str
    ministry: Optional[str] = None
    government_level: str
    state: Optional[str] = None
    district: Optional[str] = None
    pio_designation: Optional[str] = None
    address: Optional[str] = None
    online_portal: Optional[str] = None
    verification_status: str
    source_url: str
    source_title: Optional[str] = None
    last_verified: datetime

class AuthoritySearchResponse(BaseModel):
    results: List[AuthorityResponse]

class AuthorityResolution(BaseModel):
    match_status: str # MATCHED, MULTIPLE_MATCHES, NO_MATCH, NEEDS_REVIEW
    authority_id: Optional[str] = None
    confidence: str # HIGH, MEDIUM, LOW
    verification_status: Optional[str] = None
    reason: str
    warnings: List[str] = []
    missing_information: List[str] = []

# --- Phase 5 Schemas ---

class VerifiedAuthorityContext(BaseModel):
    department: str
    ministry: Optional[str] = None
    government_level: str
    state: Optional[str] = None
    district: Optional[str] = None
    pio_designation: Optional[str] = None
    appellate_authority_designation: Optional[str] = None
    address: Optional[str] = None
    filing_fee: Optional[str] = None
    payment_methods: Optional[str] = None
    online_portal: Optional[str] = None
    source_url: str
    last_verified: datetime
    verification_status: str

class DocumentGenerateRequest(BaseModel):
    language: str = "english"

class DocumentQualityResult(BaseModel):
    is_valid: bool
    score: int
    issues: List[str] = []
    suggestions: List[str] = []
    exempt_risk: Optional[str] = None
    reviewer_notes: Optional[str] = None

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    case_id: str
    document_type: str
    status: str
    title: Optional[str] = None
    content: Optional[str] = None
    language: str
    version: str
    quality_score: Optional[str] = None
    authority_snapshot: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# --- Phase 6 Schemas ---
class FilingCreate(BaseModel):
    filing_date: date
    filing_method: str
    reference_number: Optional[str] = None
    notes: Optional[str] = None

class FilingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    case_id: str
    document_id: str
    filing_date: date
    filing_method: str
    reference_number: Optional[str] = None
    acknowledgement_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

class DeadlineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    case_id: str
    filing_id: str
    deadline_type: str
    trigger_date: date
    due_date: date
    status: str
    completed_at: Optional[datetime] = None
    created_at: datetime

class CaseTimelineResponse(BaseModel):
    filing: Optional[FilingResponse] = None
    deadlines: List[DeadlineResponse] = []
    events: List[CaseEventResponse] = []
    current_status: str
    remaining_days: Optional[int] = None

# --- Phase 7 Schemas ---
class RequestMapping(BaseModel):
    request_text: str
    status: str
    evidence_excerpt: Optional[str] = None
    page_number: Optional[int] = None
    is_ocr_derived: Optional[bool] = None

class ResponseAnalysisResult(BaseModel):
    status: str
    answered: List[str]
    not_answered: List[str]
    recommended_action: str
    request_mapping: List[RequestMapping] = []
    review_required: Optional[bool] = False

class ResponseAnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    case_id: str
    document_id: str
    status: str
    answered: List[str]
    not_answered: List[str]
    recommended_action: str
    request_mapping: Optional[List[RequestMapping]] = []
    created_at: datetime

# --- Phase 8 Schemas ---
class AppealConfirmRequest(BaseModel):
    appeal_type: str

class AppealResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    case_id: str
    appeal_type: str
    status: str
    parent_document_id: str
    parent_response_document_id: str
    response_analysis_id: str
    appellate_authority_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# --- Phase 9 Schemas ---
class UserRegisterRequest(BaseModel):
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime

# --- Phase 11 Schemas ---
class AuthorityVerificationRequest(BaseModel):
    source_url: str
    source_type: str
    notes: Optional[str] = None

class AuthorityUnverificationRequest(BaseModel):
    reason: str
    new_status: str = "NEEDS_REVIEW"

class AuthorityHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    authority_id: str
    source_url: str
    source_type: str
    verification_status: str
    verified_at: datetime
    verified_by: str
    notes: Optional[str] = None

class AuthorityCreateRequest(BaseModel):
    department: str
    government_level: str
    source_url: str
    source_type: str
    ministry: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    pio_designation: Optional[str] = None
    address: Optional[str] = None
    online_portal: Optional[str] = None
    filing_fee: Optional[str] = None
    verification_notes: Optional[str] = None

class AuthorityUpdateRequest(BaseModel):
    department: Optional[str] = None
    government_level: Optional[str] = None
    ministry: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    pio_designation: Optional[str] = None
    address: Optional[str] = None
    online_portal: Optional[str] = None
    filing_fee: Optional[str] = None

class AuthorityImportRecord(BaseModel):
    department: str
    government_level: str
    source_url: str
    source_type: str
    ministry: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    office_name: Optional[str] = None
    pio_designation: Optional[str] = None
    pio_name: Optional[str] = None
    appellate_authority_designation: Optional[str] = None
    address: Optional[str] = None
    online_portal: Optional[str] = None
    filing_fee: Optional[str] = None
    payment_methods: Optional[str] = None
    verification_status: Optional[str] = "UNVERIFIED"
    verification_notes: Optional[str] = None

class AuthorityImportResult(BaseModel):
    index: int
    status: str # IMPORTED, REJECTED, POSSIBLE_DUPLICATE
    reason: Optional[str] = None
    authority_id: Optional[str] = None

class AuthorityImportRequest(BaseModel):
    records: List[AuthorityImportRecord]

class AuthorityImportResponse(BaseModel):
    total_processed: int
    imported: int
    rejected: int
    possible_duplicates: int
    results: List[AuthorityImportResult]

# --- Phase 17 Schemas (Source Intelligence) ---
class OfficialAuthoritySourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    authority_id: str
    source_url: str
    source_type: str
    is_active: bool
    last_fetch_status: Optional[str] = None
    last_fetch_error: Optional[str] = None
    last_successful_fetch_at: Optional[datetime] = None
    last_checked_at: Optional[datetime] = None
    last_parse_status: Optional[str] = None
    last_content_hash: Optional[str] = None
    last_extracted_text: Optional[str] = None
    previous_extracted_text: Optional[str] = None
    diff_summary: Optional[str] = None
    review_status: str

class SourceDecisionRequest(BaseModel):
    decision: str # IRRELEVANT_CHANGE or AUTHORITY_CHANGED
    notes: Optional[str] = None

class ProposedAuthorityChangeResponse(BaseModel):
    id: str
    source_id: str
    authority_id: str
    field_name: str
    old_value: Optional[str] = None
    proposed_value: Optional[str] = None
    evidence_snippet: Optional[str] = None
    change_type: str
    confidence: str
    review_status: str
    created_at: datetime
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class ProposedAuthorityChangeReviewRequest(BaseModel):
    decision: str # ACCEPT, REJECT, MARK_AMBIGUOUS
    notes: Optional[str] = None
