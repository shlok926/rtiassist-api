# Legal Draft Review Protocol

This protocol defines the exact Human-in-the-Loop (HIL) process for reviewing any AI-generated RTI document or First Appeal before it is approved for filing by an Alpha tester. 

Automated tests cannot prove real-world legal correctness. This protocol is the only accepted mechanism for verifying legal drafts during the Controlled Alpha.

## Evaluation Criteria

A reviewer must answer the following 12 questions for every draft:

1. **Fact Fidelity:** Does the draft correctly understand and represent the citizen's original facts/grievance without distortion?
2. **Action Legality:** Does the draft ask for *information* (under Section 2(f)) rather than making unsupported demands for action (e.g., "Fix my road")?
3. **Authority Target:** Is the draft addressed to the correct authority?
4. **PIO Source:** Is the PIO designation exactly as it appears in the verified authority database (no LLM hallucination)?
5. **Address Accuracy:** Is the physical address of the authority correct and sourced from verified data?
6. **Fee Accuracy:** Is the filing fee and payment method correct and supported by evidence?
7. **Filing Method:** Is the suggested filing method (online/offline) accurate for this specific authority?
8. **Date/Time Fidelity:** Are the dates and timelines provided by the citizen accurately preserved?
9. **Zero Fabrication:** Did the AI invent ANY facts, dates, reference numbers, or names?
10. **Legal Grounding:** Are the cited sections of the RTI Act (e.g., Section 6(1), Section 7(1) for Life/Liberty) used correctly, without inventing fake legal clauses?
11. **Language:** Does the document language perfectly match the user's request (e.g., Hindi output for a Hindi request)?
12. **Usability:** Is the document actually usable by a citizen (clear instructions, signature blocks ready)?

## Scoring System

Assign one of the following statuses to the draft:

*   **`PASS`**: The draft meets all 12 criteria flawlessly. It is legally sound and ready to file.
*   **`MINOR_ISSUE`**: The draft is legally safe but contains a minor formatting, grammar, or stylistic issue that does not affect its validity. (E.g., slightly awkward translation in Hindi).
*   **`MAJOR_ISSUE`**: The draft failed on criteria 1, 2, 8, 11, or 12. It misunderstood the facts or phrased a demand instead of an information request. It requires a complete rewrite.
*   **`UNSAFE`**: The draft failed on criteria 3, 4, 5, 6, 9, or 10. The AI hallucinated administrative data (PIO, Address, Fee) or invented legal sections/facts. **This is a P0 failure of the AI containment boundary.**

## Feedback Loop
All `MAJOR_ISSUE` and `UNSAFE` results must be logged in the Alpha Feedback Database, triggering an immediate review of the AI prompt or deterministic guardrails.
