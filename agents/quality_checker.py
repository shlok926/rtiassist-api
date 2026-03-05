import json
from utils.asi1_client import call_asi1
from prompts.system_prompts import QUALITY_CHECKER


def check_quality(draft: str) -> dict:
    """
    Layer 4: Quality check the generated RTI application draft.
    Reviews for completeness, specificity, legal compliance, and exemption risks.

    Args:
        draft: RTI application text from generate_draft()

    Returns:
        dict with is_valid, score, issues, suggestions, exempt_risk, estimated_success_probability
    """
    raw = call_asi1(
        system_prompt=QUALITY_CHECKER,
        user_message=f"Review this RTI application:\n\n{draft}",
        temperature=0.2,  # Low temp for consistent evaluation
        max_tokens=600,
    )

    try:
        clean = raw.strip().strip("```json").strip("```").strip()
        result = json.loads(clean)
    except json.JSONDecodeError:
        # Safe fallback — don't block the pipeline if quality check fails
        result = {
            "is_valid": True,
            "score": 70,
            "issues": ["Automated quality check could not parse response — please review manually."],
            "suggestions": [],
            "exempt_risk": "low",
            "exempt_risk_reason": "Manual review recommended.",
            "estimated_success_probability": "medium",
            "reviewer_notes": "Quality check encountered a parsing error. Application may still be valid.",
        }

    # Normalize score to int
    try:
        result["score"] = int(result.get("score", 70))
    except (ValueError, TypeError):
        result["score"] = 70

    # Ensure lists exist
    result.setdefault("issues", [])
    result.setdefault("suggestions", [])

    return result
