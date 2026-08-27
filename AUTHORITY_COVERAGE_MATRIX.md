# Authority Coverage Matrix

This matrix documents the exact status of authorities currently seeded in the system.

## VERIFIED Authorities

These authorities have been independently validated against official sources and are cleared for Automated Document Generation.

| Authority | Gov Level | PIO Scope | FAA Scope | Source URL | Verification Status | Limitations |
|---|---|---|---|---|---|---|
| Prime Minister's Office | Central | Centralized (Under Sec) | Centralized (Director) | `pmindia.gov.in/en/right-to-information-rti/` | **VERIFIED** | None. Single central PIO structure works. |
| Reserve Bank of India | Central | Nodal CPIO (Mumbai) | First Appellate Authority, RIA | `rbi.org.in/Scripts/Righttoinfoact.aspx` | **VERIFIED** | None. Centralized routing established. |
| Election Commission of India | Central | PIO (Nirvachan Sadan) | First Appellate Authority | `rti.eci.gov.in` | **VERIFIED** | None. Operates independent RTI portal. |
| Unique Identification Authority of India (UIDAI) | Central | CPIO (HQ) | First Appellate Authority | `uidai.gov.in` | **VERIFIED** | Local regional issues may require regional PIOs, but central handles routing. |

## NEEDS_REVIEW Authorities

These authorities are present in the database but have been explicitly restricted due to fragmented administrative structures.

| Authority | Gov Level | PIO Scope | Source URL | Verification Status | Limitations |
|---|---|---|---|---|---|
| Ministry of Railways | Central | Fragmented by Directorate/Zone | `indianrailways.gov.in` | **NEEDS_REVIEW** | The Ministry does not have a single PIO. User must specify the exact Railway Zone or Board Directorate. |
| Delhi Police | State | Fragmented by District/Unit | `delhipolice.gov.in/rti` | **NEEDS_REVIEW** | A generic "Delhi Police" RTI will be rejected. Must map to specific DCP/District PIOs. |
| Brihanmumbai Municipal Corporation (BMC) | State | Fragmented by Ward/Department | `portal.mcgm.gov.in` | **NEEDS_REVIEW** | Extremely fragmented. PIOs are split by Administrative Wards (e.g., K/West, H/East). |
| Central Board of Secondary Education (CBSE) | Central | Fragmented by Regional Office | `cbse.gov.in` | **NEEDS_REVIEW** | Mandatory routing to specific regional CPIOs based on query subject. |
