# Controlled Alpha Plan

## 1. Alpha Scope Restriction
The Alpha test is STRICTLY limited to the subset of authorities that have been manually audited and marked `VERIFIED`. 
Currently, this includes:
- Prime Minister's Office (PMO)
- Reserve Bank of India (RBI)

Any query routing to unverified authorities (like Railways or BMC) will correctly hit the fail-closed `AUTHORITY_REVIEW_REQUIRED` state and wait for an administrator to verify the dataset. **Do not bypass this boundary.**

## 2. Human-in-the-Loop (HIL) Protocol
During the Alpha, the system must maintain the explicit UI warning:
`"AI-generated draft — verify all details before submission."`

For every generated RTI/Appeal document, an Alpha reviewer (human) must check the following 10 points before marking it safe to file:
1. Citizen facts accurately represented.
2. Requested information clearly and legally phrased.
3. Authority name correct.
4. PIO designation correct.
5. Office Address matches official data.
6. Filing Fee information correct.
7. Filing method (Online/Offline) valid.
8. Language matches requested output (English/Hindi).
9. **No fabricated facts** (AI did not invent a grievance or date).
10. **No fabricated legal claims** (AI did not invent fake sections of the RTI Act).

## 3. Alpha User Feedback Protocol
Alpha users will have a streamlined method to categorize their feedback. If an RTI generation fails or produces poor output, the user should categorize it as:
- Wrong understanding
- Missing clarification
- Wrong action recommendation
- Wrong authority
- Authority unavailable
- Draft quality issue
- Incorrect legal statement
- OCR issue
- Response analysis issue
- Appeal issue
- UX confusion
- Filing confusion
- Other

## 4. Minimum Viable Backup & Recovery Drill
Before launching, the administrator must run a simulated disaster recovery drill. 
**Procedure:**
1. Generate a database backup using `pg_dump` (or `sqlite3 .backup` for local).
2. Wipe the current database.
3. Restore using `pg_restore`.
4. Run Alembic migrations: `python -m alembic upgrade head`.
5. Start the application.
6. Verify Case, Document, and Timeline retrieval for an existing user.
*(A log of this drill must be maintained).*
