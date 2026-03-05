from pydantic import BaseModel, Field
from typing import List, Optional


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
        description="Language for the RTI draft: 'english' or 'hindi'",
    )
    state: Optional[str] = Field(
        default=None,
        description="State name if filing a state-level RTI. Leave blank for Central Government.",
        example="Maharashtra",
    )
    demo_mode: bool = Field(
        default=False,
        description="Enable demo mode for instant sample responses without API calls",
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
