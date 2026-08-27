# Phase 16 Production Audit

## 1. Secrets & Configuration
- **JWT_SECRET_KEY**: Properly protected. Raises `ValueError` in production if absent.
- **CORS_ORIGINS**: Currently defaults to `"*"` via `os.getenv("CORS_ORIGINS", "*")`. **[P1 - Production Blocker]**: Allowing `*` in production is a massive CSRF/Data leakage risk. It must default to a secure internal or restricted list in production or fail to boot.
- **DEBUG Routes**: Routes like `/debug/webhook` correctly assert `ENVIRONMENT != "development"`. Safe.

## 2. Dependencies & Migrations
- **Alembic**: Missing from `requirements.txt`. **[P1 - Production Blocker]**: Without Alembic, production schema migrations will fail.
- **OCR Engine**: `pdfplumber` is present, but `pytesseract` and `Pillow` are absent from `requirements.txt`. **[P1 - Production Blocker]**: Fallback OCR will crash if dependencies are missing.
- **PostgreSQL Support**: Missing `psycopg2-binary`. **[P2 - Operational Weakness]**: Cannot switch away from SQLite without driver.

## 3. Rate Limiting & Abuse
- No explicit rate-limiting middleware exists on LLM generation endpoints. **[P2 - Operational Weakness]**: Generative endpoints (`/cases/{id}/recommend-action`, `/cases/{id}/generate-document`) are vulnerable to simple flooding which can exhaust LLM tokens or billings.

## 4. File Upload Paths
- PDF validation correctly bounds at 10MB and checks Magic Bytes.
- Temp files are safely created and cleaned via `try/finally` in `Response Service`. Safe.

## 5. Database Transactions
- Case status transitions are generally safe. For instance, document generation creates intermediate saves. If a failure occurs before completion, the Case state does NOT advance erroneously to `READY_TO_FILE`.
- The commit chunks are small and frequent, reducing deadlocks. Safe.

## 6. LLM Reliability
- `asi1_client.py` implements bounded retries (3 attempts).
- Fallbacks correctly return HTTP 500s on failure, preventing hallucinated legal advice. Safe.

## 7. Web <-> Telegram Parity
- Needs empirical testing to ensure `telegram_id` correctly enforces case boundaries seamlessly.

## Action Plan
- **Fix P1s**: Enforce strict `CORS`, add `alembic` and OCR tools to `requirements.txt`.
- **Address P2s**: Add `psycopg2-binary` for deployment readiness.
- Execute Web <-> Telegram parity tests to validate Transport decoupling.
