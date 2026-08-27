# Alpha Telemetry Specification

To observe the Alpha phase safely without introducing massive analytics platforms or violating privacy, we will log AI behaviors explicitly using structured Python `logging` attached to unique Request IDs.

## Data Points to Capture Safely
For every AI operation (Intent Classification, Authority Resolution, Document Drafting, OCR, Response Analysis):

*   **Request ID**: Unique UUID correlating all events in a single HTTP request lifecycle.
*   **Case ID**: The affected Case UUID.
*   **Timestamp**: UTC ISO-8601.
*   **Operation Type**: e.g., `INTENT_CLASSIFICATION`, `DRAFT_GENERATION`.
*   **Model/Provider**: e.g., `asi1-mini`.
*   **Success/Failure**: Boolean or HTTP-equivalent status.
*   **Latency**: Execution time in milliseconds.
*   **Structured Output Validation Result**: Did Pydantic parse the LLM JSON successfully? (`True`/`False`)
*   **Fallback Used**: Did the system use a fallback prompt or mechanism? (`True`/`False`)
*   **Clarification Requested**: Did the AI pause for citizen clarification? (`True`/`False`)
*   **Confidence**: AI's self-reported confidence score (0.0 to 1.0).
*   **Human-Review Required**: Was the result flagged for manual review? (`True`/`False`)

## Privacy & Security Hard Boundaries
The telemetry system MUST NEVER log:
1. Passwords or password hashes.
2. JWT tokens or session keys.
3. API credentials (e.g., LLM keys, Telegram tokens).
4. Unnecessary PII (citizen names, emails, physical addresses).
5. Full text of sensitive documents unless explicitly required for debugging a specific `OCR_FAILURE` (and then, only temporarily).

## Sample Log Format
```json
{
  "request_id": "req-1234-abcd",
  "timestamp": "2026-08-27T18:05:00Z",
  "level": "INFO",
  "event_type": "AI_TELEMETRY",
  "operation": "AUTHORITY_RESOLUTION",
  "case_id": "case-999",
  "model": "asi1-mini",
  "success": true,
  "latency_ms": 1245,
  "validation_passed": true,
  "fallback_used": false,
  "confidence": 0.95,
  "human_review_required": false
}
```
