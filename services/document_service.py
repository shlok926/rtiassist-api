import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone
from models.orm.case import Case
from models.orm.document import Document
from models.orm.case_event import CaseEvent
from models.schemas import DocumentGenerateRequest, DocumentResponse, DocumentQualityResult, VerifiedAuthorityContext
from services.case_service import get_case
from repositories import authority_repository
from agents import draft_generator, quality_checker

def get_document(db: Session, case_id: str, document_id: str, user_id: str) -> Document:
    case = get_case(db, case_id, user_id)
    doc = db.query(Document).filter(Document.id == document_id, Document.case_id == case.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

def generate_case_document(db: Session, case_id: str, user_id: str, request: DocumentGenerateRequest) -> DocumentResponse:
    # 1. Load Case
    case = get_case(db, case_id, user_id)
    
    # 2. Verify prerequisites
    if case.status not in ["AUTHORITY_RESOLVED", "READY_TO_FILE", "DOCUMENT_NEEDS_REVISION"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot generate document in current state: {case.status}. Expected AUTHORITY_RESOLVED."
        )
        
    action = case.recommended_action
    if not action or action not in ["RTI"]:
        raise HTTPException(status_code=400, detail="UNSUPPORTED_ACTION")
        
    if not case.authority_id:
        raise HTTPException(status_code=400, detail="AUTHORITY_NOT_RESOLVED")
        
    authority = authority_repository.get_by_id(db, case.authority_id)
    if not authority or authority.verification_status != "VERIFIED" or not authority.active:
        raise HTTPException(status_code=400, detail="AUTHORITY_REVIEW_REQUIRED")
        
    # 3. Construct Authority Context
    auth_ctx = VerifiedAuthorityContext(
        department=authority.department,
        ministry=authority.ministry,
        government_level=authority.government_level,
        state=authority.state,
        district=authority.district,
        pio_designation=authority.pio_designation,
        appellate_authority_designation=authority.appellate_authority_designation,
        address=authority.address,
        filing_fee=authority.filing_fee,
        payment_methods=authority.payment_methods,
        online_portal=authority.online_portal,
        source_url=authority.source_url,
        last_verified=authority.last_verified,
        verification_status=authority.verification_status
    )
    
    auth_dict = auth_ctx.model_dump(mode='json')
    
    # Log Generation Started
    db.add(CaseEvent(
        case_id=case.id,
        event_type="DOCUMENT_GENERATION_STARTED",
        description=f"Starting generation of {action} in {request.language}",
    ))
    db.commit()
    
    # 4. Generate Draft
    try:
        draft_content = draft_generator.generate_case_draft(
            problem_description=case.problem_description,
            action=action,
            authority_context=auth_dict,
            language=request.language
        )
    except Exception as e:
        db.add(CaseEvent(
            case_id=case.id,
            event_type="DRAFT_GENERATION_FAILED",
            description=str(e),
        ))
        db.commit()
        raise HTTPException(status_code=500, detail="DRAFT_GENERATION_FAILED")
        
    # Check if this is a revision
    existing_docs = db.query(Document).filter(Document.case_id == case.id, Document.document_type == action).all()
    version = f"v{len(existing_docs) + 1}"
    
    # 5. Quality Check
    try:
        quality_raw = quality_checker.check_quality(draft_content)
        quality_result = DocumentQualityResult(**quality_raw)
    except Exception as e:
        db.add(CaseEvent(
            case_id=case.id,
            event_type="QUALITY_CHECK_FAILED",
            description=str(e),
        ))
        db.commit()
        raise HTTPException(status_code=500, detail="QUALITY_CHECK_FAILED")

    # 6. Persist Document & State
    doc = Document(
        case_id=case.id,
        document_type=action,
        title=f"{action} Application - {version}",
        content=draft_content,
        language=request.language,
        version=version,
        authority_snapshot=json.dumps(auth_dict),
        generation_context={
            "case_facts": case.extracted_facts,
            "case_objective": case.case_objective,
            "action": action,
            "language": request.language,
            "verified_authority": auth_dict
        },
        generated_from_case_version=str(case.updated_at.isoformat()) if case.updated_at else None
    )
    
    doc.quality_score = str(quality_result.score)
    doc.quality_check_result = quality_raw
    
    if quality_result.is_valid and quality_result.score >= 70:
        doc.status = "READY_TO_FILE"
        case.status = "READY_TO_FILE"
        event_type = "DOCUMENT_READY_TO_FILE"
    else:
        doc.status = "NEEDS_REVISION"
        case.status = "DOCUMENT_NEEDS_REVISION"
        event_type = "DOCUMENT_NEEDS_REVISION"

    db.add(doc)
    # Flush to get doc.id
    db.flush()
    
    db.add(CaseEvent(
        case_id=case.id,
        event_type="DOCUMENT_GENERATED",
        description=f"Draft generated successfully ({version})",
        event_metadata={"document_id": doc.id}
    ))
    
    db.add(CaseEvent(
        case_id=case.id,
        event_type=event_type,
        description=f"Quality check completed. Score: {quality_result.score}",
        event_metadata={"quality_result": quality_result.model_dump(mode='json')}
    ))
    db.commit()
    db.refresh(doc)
    
    return DocumentResponse.model_validate(doc)
