import json
from models.schemas import ResponseAnalysisResult
from utils.llm_parser import parse_llm_json
from utils.asi1_client import call_asi1

def analyze_response(problem_description: str, rti_content: str, government_response_text: str) -> dict:
    """
    Analyzes the government response against the original problem and the filed RTI.
    Classifies the response and recommends next actions.
    """
    prompt = f"""
    You are an expert Indian legal analyst specializing in RTI (Right to Information).
    
    ORIGINAL CITIZEN PROBLEM:
    {problem_description}
    
    FILED RTI DOCUMENT CONTENT:
    {rti_content}
    
    GOVERNMENT RESPONSE RECEIVED:
    {government_response_text}
    
    Your task is to analyze the government response to determine if it satisfactorily answers the RTI request.
    Extract what was answered and what was NOT answered.
    Determine the overall status: ANSWERED, PARTIALLY_ANSWERED, NOT_ANSWERED, DENIED, or IRRELEVANT.
    Recommend the next administrative action: CLOSE_CASE, REQUEST_CLARIFICATION, FOLLOW_UP, FIRST_APPEAL, or NEEDS_HUMAN_REVIEW.
    
    CRITICAL: For every specific information request in the FILED RTI DOCUMENT, map it to the government response. Provide the text of the original request, its status, and the evidence excerpt from the government response. Do not invent page numbers. If unsure of page, leave it null. If the text appears to be from a low-quality OCR (e.g. lots of typos), set is_ocr_derived to true.
    
    Return the result strictly as a valid JSON object matching the following structure exactly, with no additional text or markdown formatting:
    {{
        "status": "PARTIALLY_ANSWERED",
        "answered": ["List of points the government successfully answered"],
        "not_answered": ["List of points they missed, ignored, or denied"],
        "recommended_action": "FIRST_APPEAL",
        "request_mapping": [
            {{
                "request_text": "Copy of the file noting",
                "status": "ANSWERED",
                "evidence_excerpt": "Enclosed on page 3...",
                "page_number": 3,
                "is_ocr_derived": false
            }}
        ],
        "review_required": false
    }}
    """
    
    try:
        response_text = call_asi1(prompt)
        parsed_json = parse_llm_json(response_text)
        
        # Validate against schema to ensure correctness
        result = ResponseAnalysisResult(**parsed_json)
        return result.model_dump()
        
    except Exception as e:
        # Fallback if something fails
        return {
            "status": "ANALYSIS_FAILED",
            "answered": [],
            "not_answered": ["Failed to parse response automatically"],
            "recommended_action": "NEEDS_HUMAN_REVIEW",
            "request_mapping": [],
            "review_required": True
        }
