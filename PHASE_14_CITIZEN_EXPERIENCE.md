# Phase 14: Citizen Experience Layer

## Overview
Phase 14 focuses on surfacing the Phase 13 Case Intelligence layers into the citizen-facing React UI, turning the backend's internal understanding into a visible and actionable experience. It adheres to the primary architectural rule: **Backend remains the SINGLE SOURCE OF TRUTH.** 

The new experience introduces `CaseDetail.jsx` as the central citizen workspace where the user can manage the journey of their RTI case across understanding, recommendation, authority resolution, document drafting, filing, tracking, and response analysis.

## Frontend Architecture
We evolved the existing React Application without tearing down the existing infrastructure. We leveraged the current navigation structure (`activeTab`) to seamlessly introduce a new `case-detail` view.
- `RTIForm.jsx` automatically creates the case and redirects the user to the `CaseDetail` view, initiating their guided journey.
- `Tracker.jsx` now uses a simplified "View Case" button which drops the user directly into their `CaseDetail` workspace, delegating status and lifecycle updates fully to the backend.

## Case Detail Experience
The core of Phase 14 resides in `src/components/case/CaseDetail.jsx`. This acts as a single-page workspace where citizens track their issue end-to-end. It uses progressive disclosure to only show what is relevant to the case's current lifecycle state.

### Fact Confirmation
When an RTI/Grievance problem is submitted, the frontend displays: "Here's what we understood."
It displays the AI-extracted `case_objective` and structured `extracted_facts` directly mapped from the backend, providing a "Confirm Understanding" step before moving forward.

### Action Recommendation
Based on the problem, a recommendation is rendered prominently (e.g., "RTI" or "PUBLIC_GRIEVANCE"). The citizen must explicitly hit "Confirm Action" before they progress, satisfying the rule against over-automation.

### Clarification
If the `NEEDS_CLARIFICATION` state is encountered, it halts the workflow with a yellow warning, informing the user that more information is needed without crashing the process.

### Case Journey & Tracker
The overall progression of states (`UNDERSTANDING` -> `ACTION_RECOMMENDED` -> `READY_TO_FILE` -> `FILED` -> `RESPONSE_RECEIVED`) is visually translated to citizen-friendly labels like "Waiting for government response". The legacy tracker state mutation was stripped out—everything now hinges on backend validation.

### Response Mapping
When an official government response is analyzed, the frontend renders a detailed summary of the `request_mapping`. It shows:
- What questions were asked (Your request #1)
- What status they have (Answered, Partially answered, Not answered, Denied)
- The evidence excerpt and the page number
- Whether the evidence was derived through OCR

### Human Review & Next Action
Any low-confidence authority matches or complex cases display specific warning blocks.
Finally, when the response analysis is ready, the frontend renders the next step. If it is `FIRST_APPEAL`, the citizen can proceed to start an appeal right from the analysis block.

## Accessibility & Security
- Leveraged clear hierarchical coloring (green for verified/positive, yellow for warnings, red for errors) to increase scanning readability.
- Re-used JWT authentication and case-specific `caseId` paths, relying strictly on standard React states preventing unauthenticated exposure.
- Safe file uploads via standard HTML forms directly to the secure API.

## Known Limitations
- Modifying exact facts individually via a rich form editor is not implemented in favor of a simpler "Confirm Understanding" approach. (Full individual field editing can be added easily based on the unified Patch endpoint).
- Mobile responsive layout is functional but could benefit from stricter padding scaling for highly complex responses.
- Timeline only shows the current state and next deadline. Full detailed event logging history could be surfaced inside an accordion.
