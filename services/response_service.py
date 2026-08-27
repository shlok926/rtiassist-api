import os
import tempfile
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from models.orm.document import Document
from models.orm.case_event import CaseEvent
from models.orm.response_analysis import ResponseAnalysis
from services.case_service import get_case
from services.ocr_service import OCRService
from agents.response_analyzer import analyze_response
from models.schemas import ResponseAnalysisResponse

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def upload_and_analyze_response(db: Session, case_id: str, user_id: str, file: UploadFile) -> ResponseAnalysisResponse:
    # 1. Verify case
    case = get_case(db, case_id, user_id)
    if case.status != "AWAITING_RESPONSE":
        raise HTTPException(status_code=400, detail="Case is not awaiting a response.")
        
    # 2. Extract Text
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed for responses.")
        
    temp_path = None
    extracted_text = ""
    try:
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, "wb") as f:
            chunk = await file.read(1024 * 1024)
            if not chunk or not chunk.startswith(b'%PDF'):
                raise HTTPException(status_code=400, detail="Invalid PDF file signature")
                
            total_size = len(chunk)
            f.write(chunk)
            
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large.")
                f.write(chunk)
                
        ocr_service = OCRService()
        extraction_result = ocr_service.extract_text(temp_path)
        extracted_text = extraction_result.get("text", "")
        extraction_metadata = {
            "method": extraction_result.get("method"),
            "ocr_used": extraction_result.get("ocr_used"),
            "page_count": extraction_result.get("page_count"),
            "extraction_warning": extraction_result.get("extraction_warning")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process PDF.")
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
                
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the PDF.")
        
    # 3. Create Document representing the Government Response
    # The Document table is used here to store the response content.
    doc = Document(
        case_id=case.id,
        document_type="GOVERNMENT_RESPONSE",
        content=extracted_text,
        language="english", # default assumption
        version=1,
        extraction_metadata=extraction_metadata
    )
    db.add(doc)
    db.flush()
    
    # Update Case status to RESPONSE_RECEIVED
    case.status = "RESPONSE_RECEIVED"
    
    db.add(CaseEvent(
        case_id=case.id,
        event_type="RESPONSE_RECEIVED",
        description=f"Received government response: {file.filename}",
        event_metadata={"document_id": doc.id}
    ))
    db.commit()
    
    # 4. Find the filed RTI Document to compare against
    rti_doc = next((d for d in case.documents if d.document_type == "RTI" and d.status == "READY_TO_FILE"), None)
    rti_content = rti_doc.content if rti_doc else "Unknown filed content."
    
    # 5. Run Analysis Agent
    analysis_dict = analyze_response(
        problem_description=case.problem_description,
        rti_content=rti_content,
        government_response_text=extracted_text
    )
    
    # 6. Store ResponseAnalysis
    import json
    analysis = ResponseAnalysis(
        case_id=case.id,
        document_id=doc.id,
        status=analysis_dict.get("status", "ANALYSIS_FAILED"),
        answered=analysis_dict.get("answered", []),
        not_answered=analysis_dict.get("not_answered", []),
        recommended_action=analysis_dict.get("recommended_action", "NEEDS_HUMAN_REVIEW")
    )
    request_mapping_raw = analysis_dict.get("request_mapping", [])
    if request_mapping_raw:
        # Convert RequestMapping objects (if any) or dicts to JSON-serializable list
        mapping_dicts = []
        for r in request_mapping_raw:
            if hasattr(r, 'model_dump'):
                mapping_dicts.append(r.model_dump())
            else:
                mapping_dicts.append(r)
        analysis.request_mapping = mapping_dicts
    else:
        analysis.request_mapping = []
    db.add(analysis)
    
    # 7. Update Case State & Event
    if analysis.status in ["ANSWERED", "PARTIALLY_ANSWERED", "NOT_ANSWERED", "DENIED", "IRRELEVANT"]:
        case.status = "ANALYSIS_READY"
        case.next_action_recommendation = analysis.recommended_action
        
        # If action is appeal, transition further? We leave it at ANALYSIS_READY so user can view it first.
        
    db.add(CaseEvent(
        case_id=case.id,
        event_type="ANALYSIS_READY",
        description=f"Response analysis completed. Status: {analysis.status}",
        event_metadata={"analysis_id": analysis.id, "recommended_action": analysis.recommended_action}
    ))
    
    db.commit()
    db.refresh(analysis)
    
    return ResponseAnalysisResponse.model_validate(analysis)
