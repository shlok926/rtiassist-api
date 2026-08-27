from utils.asi1_client import call_asi1

def generate_first_appeal(
    original_problem: str,
    original_rti: str,
    government_response: str,
    request_mapping: list,
    recommended_action: str,
    appellate_authority_department: str,
    language: str = "english"
) -> str:
    
    import json
    request_mapping_str = json.dumps(request_mapping, indent=2)
    
    prompt = f"""
    You are an expert Indian legal drafter specializing in RTI First Appeals.
    
    ORIGINAL PROBLEM:
    {original_problem}
    
    ORIGINAL RTI APPLICATION:
    {original_rti}
    
    GOVERNMENT RESPONSE:
    {government_response}
    
    RESPONSE ANALYSIS (Request-by-Request Mapping):
    {request_mapping_str}
    
    APPELLATE AUTHORITY:
    {appellate_authority_department}
    
    Draft a formal First Appeal under Section 19(1) of the RTI Act, 2005.
    The appeal must be grounded strictly in the response analysis.
    Do NOT invent new facts, allegations, or fabricated government statements.
    Focus on the unanswered/denied points.
    
    Write the appeal in {language}.
    Output ONLY the raw text of the drafted document. No conversational filler, no markdown blocks.
    """
    
    raw = call_asi1(
        system_prompt="You are a strict, formal legal drafting assistant. Output only the requested document text.",
        user_message=prompt,
        temperature=0.3,
        max_tokens=2000
    )
    return raw.strip()
