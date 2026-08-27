# Alpha Failure Taxonomy

This taxonomy categorizes operational, architectural, and AI failures expected during the Controlled Alpha. Use these standard labels in all defect reports and telemetry.

## 1. AI and Extraction Failures
*   **`AI_FAILURE`**: General failure of the LLM to return a valid response, timeout, or parsing error.
*   **`FACT_EXTRACTION_ERROR`**: AI failed to extract explicitly stated citizen facts or extracted them incorrectly.
*   **`DRAFT_QUALITY_FAILURE`**: AI generated a draft that is legally incorrect, grammatically flawed, or hallucinates administrative data despite fail-closed guardrails.
*   **`OCR_FAILURE`**: Vision/OCR system failed to extract text from a provided government response document.
*   **`OCR_REVIEW_REQUIRED`**: OCR succeeded partially but confidence is low or text is mangled, requiring human fallback.
*   **`RESPONSE_ANALYSIS_FAILURE`**: AI incorrectly analyzed a government response (e.g., categorizing a rejection as an acceptance).

## 2. Authority Resolution Failures
*   **`AUTHORITY_NO_MATCH`**: Citizen's request relates to a department not present in the database.
*   **`AUTHORITY_MULTIPLE_MATCH`**: Request matches multiple database records ambiguously (e.g., generic "Police").
*   **`AUTHORITY_EXPIRED`**: Matched authority exists but has exceeded its verification TTL (time-to-live).
*   **`AUTHORITY_REVIEW_REQUIRED`**: Matched authority exists but is not marked `VERIFIED` (e.g., `UNVERIFIED` or `NEEDS_REVIEW`).

## 3. Operational & System Failures
*   **`USER_CORRECTION`**: Citizen explicitly rejects and corrects an AI-recommended action or fact.
*   **`DEADLINE_ERROR`**: System incorrectly calculates statutory deadlines (e.g., Section 7(1) 30-day limits).
*   **`FILING_ERROR`**: Failure in logging or tracking a filed RTI or Appeal.
*   **`AUTHORIZATION_FAILURE`**: Tenant isolation breach, IDOR, or invalid JWT usage.
*   **`RATE_LIMITED`**: Citizen or IP hits operational API quotas.
*   **`SYSTEM_ERROR`**: Unhandled exception, database connection failure, or server crash (500 Internal Server Error).
