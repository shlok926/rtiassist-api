# RTIAssist Final Go-Live Checklist

## Security
Status: PASS
Evidence: Strict domain boundaries tested; JWT authentication enforced; CORS wildcard rejected in production.

## Authentication
Status: PASS
Evidence: Standard OAuth2 Password Bearer flow with stateless JWT validation. Role-based restrictions functioning for admin paths.

## Authorization
Status: PASS
Evidence: Parity test and Security test suites demonstrate hard tenant boundaries (User A receives 404 for User B cases/documents).

## CORS
Status: PASS
Evidence: `CORS_ORIGINS` environment variable must be explicit. System fails on boot if missing or set to `*`.

## Rate limiting
Status: PASS
Evidence: Lightweight in-memory rate limiter implemented on generative endpoints, preventing unauthenticated/authenticated brute-force token depletion.

## Secrets
Status: PASS
Evidence: `JWT_SECRET_KEY` raises `ValueError` in production if absent. Passwords hashed securely using bcrypt. No keys committed.

## Database
Status: PASS
Evidence: Domain services use atomic transaction boundaries. All mutations execute exclusively via SQLAlchemy ORM safely. `psycopg2-binary` packaged for Postgres runtime.

## Alembic
Status: PASS
Evidence: Included as top-level production dependency.

## Uploads
Status: PASS
Evidence: Max 10MB chunked limits enforced. Filetype verified by both extension and `%PDF` Magic Bytes. Safe temporary file cleanup implemented using `finally` blocks.

## OCR
Status: PASS
Evidence: Graceful fallbacks implemented if Tesseract system executable is missing. Output safely parsed with page limits.

## LLM
Status: PASS
Evidence: Generation bounded by prompt wrappers, validated aggressively via Pydantic strict schemas, with 3-attempt backoff logic.

## Authority Data Architecture
Status: PASS
Evidence: Core DB functionality is verified, and the deterministic verified boundary is safely enforced by the backend.

## Authority Dataset Population
Status: DEFERRED (Required before public use)
Evidence: The system has no real-world verified authorities loaded yet. Manual administrative population is required before meaningful Alpha use.

## Human Review
Status: PASS
Evidence: The `NEEDS_REVIEW` and `OCR_REVIEW_REQUIRED` states act as manual stopgaps for unpredictable automation failures.

## Telegram
Status: PASS
Evidence: Webhook integration works identically to Web frontend via shared deterministic case workflow API endpoints. `telegram_id` effectively mapped to User model.

## Frontend
Status: PASS
Evidence: React architecture successfully intercepts Phase 14 structures; production bundles build cleanly.

## Observability
Status: PASS
Evidence: Minimalist structured JSON-ready Request ID logging middleware tracks request times. 

## Backups
Status: NOT CONFIGURED
Evidence: Deferred to cloud infrastructure provider's DB backup policies.

## Recovery
Status: DEFERRED
Evidence: Failures leave the system in deterministic previous state, but manual operations recovery documentation is not yet formally drafted for end-users.

## Testing
Status: PASS
Evidence: 83/83 core scenarios spanning logic, validation, parity, and state machines are confirmed passing natively.

## Deployment
Status: PASS
Evidence: Environment configurations map cleanly to standard PaaS/Docker expectations.

## Legal/trust UX
Status: PASS
Evidence: Disclaimers block automated filing; the citizen remains strictly in control of "Final Approval" state.
