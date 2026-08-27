# Phase 15 Validation Plan

This validation plan outlines 15 distinct real-world scenarios designed to stress-test RTIAssist across the full citizen lifecycle. 

## Scenario 01: Pure Information Request
- **Input**: "I want a copy of the approved budget and expenditure records for the municipal road project in my ward."
- **Expected Action**: `RTI` (RECORD_REQUEST)
- **Expected Clarification**: None required if minimum facts met, otherwise asks for ward name/city.
- **Expected Authority**: Municipal Corporation
- **Expected Document**: Precise RTI request citing relevant records.
- **Pass/Fail Criteria**: Must accurately classify as RTI, resolve authority correctly, and generate record-seeking text without grievance complaints.

## Scenario 02: Grievance, Not RTI
- **Input**: "The road outside my house has been damaged for six months. I want the municipality to repair it."
- **Expected Action**: `PUBLIC_GRIEVANCE`
- **Expected Authority Behavior**: Halt RTI pipeline. (Supported: false for RTI workflows).
- **Pass/Fail Criteria**: Must not automatically generate an RTI or hallucinate a legal remedy.

## Scenario 03: Grievance + Information Request
- **Input**: "My scholarship has not been credited. I want the payment processed and also want to know the current status and reason for the delay."
- **Expected Action**: `RTI` (for status/reason) or `PUBLIC_GRIEVANCE` (for payment).
- **Pass/Fail Criteria**: Must separate the desired outcome (payment) from the information objective (status), recommending a supported action without inventing workflows.

## Scenario 04: Unknown Department
- **Input**: "I applied for a government scheme but I don't know which department handles it."
- **Expected Action**: `NEEDS_CLARIFICATION`
- **Expected Clarification**: "Which specific government scheme did you apply for? (e.g., PM Kisan, PM Awas Yojana)"
- **Pass/Fail Criteria**: System must not hallucinate a department; must pause the workflow and ask for the scheme name.

## Scenario 05: Missing Application Number
- **Input**: "I applied for a new electricity meter 2 months ago in Mumbai but haven't received it. I lost my application number."
- **Expected Action**: `RTI`
- **Pass/Fail Criteria**: Must proceed and not block. The document should state "Application number unavailable/lost" and rely on date/address facts.

## Scenario 06: Incorrect PIO Provided by User
- **Input**: "The PIO is Mr. XYZ at this address."
- **Expected Action**: `RTI`
- **Expected Authority Behavior**: Must use deterministic database lookup, ignoring "Mr. XYZ" as authoritative.
- **Expected Document**: Uses DB verified PIO details.
- **Pass/Fail Criteria**: Generated document and case state must use `VERIFIED` DB authority, not the LLM/User provided one.

## Scenario 07: Ambiguous Authority
- **Input**: "I need records from the education department."
- **Expected Action**: `RTI`
- **Expected Authority Behavior**: `MULTIPLE_MATCHES` / `AUTHORITY_REVIEW_REQUIRED` (e.g., State vs Central Education Dept).
- **Pass/Fail Criteria**: Must block document generation until the user/admin selects the precise authority.

## Scenario 08: Verified Authority Expired
- **Input**: Standard valid RTI request matching an authority last verified 2 years ago.
- **Expected Authority Behavior**: `EXPIRED` or `NEEDS_REVIEW`.
- **Pass/Fail Criteria**: Must flag the authority and block automated document generation, maintaining case integrity.

## Scenario 09: Multilingual Citizen
- **Input**: "Mera ration card 3 mahine se pending hai. Kripya reason bataye."
- **Expected Action**: `RTI`
- **Expected Document**: Drafted in Hindi or English (based on selected preference) with accurately mapped deterministic authority (in English/official language).
- **Pass/Fail Criteria**: System correctly interprets Hindi input, does not translate proper nouns/authority addresses poorly.

## Scenario 10: Realistic Scanned Response
- **Input**: Upload of a synthetic scanned PDF (images inside PDF).
- **Expected Response Analysis**: Triggers OCR fallback.
- **Pass/Fail Criteria**: Must extract text using pytesseract, log `ocr_used: true`, and present `OCR_REVIEW_REQUIRED` warning to the user.

## Scenario 11: Complete Government Response
- **Input**: Synthetic PDF responding explicitly to all 3 requested points with data.
- **Expected Response Analysis**: Request mappings all `Answered`.
- **Expected Next Action**: `CLOSE_CASE` or `SATISFACTORY`.
- **Pass/Fail Criteria**: Next action must NOT be `FIRST_APPEAL`.

## Scenario 12: Partial Government Response
- **Input**: Synthetic PDF answering Point 1, ignoring Point 2.
- **Expected Response Analysis**: Point 1 `Answered`, Point 2 `Not answered`.
- **Expected Next Action**: `FIRST_APPEAL`.
- **Pass/Fail Criteria**: Must correctly identify the unanswered point.

## Scenario 13: Rejected Response
- **Input**: Synthetic PDF stating "Information denied under Section 8(1)(j)".
- **Expected Response Analysis**: Point 1 `Denied`.
- **Expected Next Action**: `FIRST_APPEAL`.
- **Pass/Fail Criteria**: Correctly attributes rejection without hallucinating additional legal opinions.

## Scenario 14: User Corrects AI Understanding
- **Input**: Initial input parsed as "Transport Dept". User updates case objective to "Municipal Corporation".
- **Expected Behavior**: New facts saved.
- **Pass/Fail Criteria**: Subsequent generation must use the corrected facts.

## Scenario 15: First Appeal Full Cycle
- **Input**: Full traversal: RTI -> Filed -> Partial Response -> Analysis -> First Appeal Recommended -> User Confirmation -> Appeal Draft.
- **Pass/Fail Criteria**: Appeal draft must reference original RTI date, exact unanswered questions from analysis, and correctly identify Appellate Authority without inventing new grievances.
