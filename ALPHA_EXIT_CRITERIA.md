# Alpha Exit Criteria (Go/No-Go)

To move the system from `CONDITIONAL GO` (Alpha) to `FULL GO` (Production-wide Beta/GA launch), the following objective, evidence-based criteria must be met.

## 1. Authority Coverage Thresholds (Provisional)
- Minimum **50 highly-requested Central Authorities** marked `VERIFIED`.
- Minimum **5 Major States** with basic nodal `VERIFIED` coverage (e.g., State Secretariat/HQ).
- Strategy implemented for fragmented authorities (e.g., Police, BMC) allowing granular ward/district selection by the user.

## 2. Usage & AI Reliability Thresholds
- Minimum **100 Human-Reviewed Alpha Cases** executed end-to-end.
- **Zero (0)** systematic authority hallucinations (e.g., AI bypassing the deterministic DB boundary).
- Acceptable `MAJOR_ISSUE` legal draft failure rate: **< 5%** (Provisional).
- Acceptable OCR failure/mangling rate: **< 10%** (Provisional).

## 3. Security & Operational Gates
- **Zero (0)** P0/P1 security findings (No IDOR, no data leakage, no unauthorized API access).
- **100%** fail-closed behavior maintained (Unverified authorities strictly block document generation).
- Successful execution of the Backup & Recovery Drill (Database restore + Alembic works flawlessly).
- Production environment variables (JWT keys, CORS, Database URLs) confirmed fully isolated from development.

## 4. UX Gates
- **Zero (0)** UX-P0 (Blocking) issues unresolved.
- Feedback loop operational and producing actionable data.
