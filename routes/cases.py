from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import Response
from models.database import get_db
from models.schemas import (CaseCreate, CaseUpdate, CaseResponse, CaseListResponse, TrackerImport, 
                            ActionRecommendation, ActionConfirmation, AuthorityResolution, 
                            DocumentGenerateRequest, DocumentResponse, FilingCreate, FilingResponse, CaseTimelineResponse, ResponseAnalysisResponse,
                            AppealConfirmRequest, AppealResponse)
from services import case_service, document_service, filing_service, response_service
from dependencies.auth import get_current_user
from dependencies.rate_limit import rate_limit_expensive
from models.orm.user import User

router = APIRouter(prefix="/cases", tags=["Cases"])

@router.post("", response_model=CaseResponse)
def create_case(case_data: CaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Initialize a new citizen problem/case."""
    return case_service.create_case(db, current_user.id, case_data)

@router.get("", response_model=CaseListResponse)
def list_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all cases belonging to the current user."""
    return case_service.get_cases(db, current_user.id, skip, limit)

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a specific case."""
    return case_service.get_case(db, case_id, current_user.id)

@router.patch("/{case_id}", response_model=CaseResponse)
def update_case(case_id: str, update_data: CaseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update editable fields of a case safely."""
    return case_service.update_case(db, case_id, current_user.id, update_data)

@router.post("/{case_id}/recommend-action", response_model=ActionRecommendation, dependencies=[Depends(rate_limit_expensive)])
def recommend_action(case_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Analyze the case problem and recommend the best legal/administrative action."""
    return case_service.recommend_action(db, case_id, current_user.id)

@router.post("/{case_id}/confirm-action", response_model=CaseResponse)
def confirm_action(case_id: str, confirmation: ActionConfirmation, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Confirm the recommended action and transition case to ACTION_CONFIRMED."""
    return case_service.confirm_action(db, case_id, current_user.id, confirmation)

@router.post("/{case_id}/resolve-authority", response_model=AuthorityResolution)
def resolve_authority(case_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Resolve the authoritative PIO/Department for this case."""
    return case_service.resolve_case_authority(db, case_id, current_user.id)

@router.post("/{case_id}/generate-document", response_model=DocumentResponse, dependencies=[Depends(rate_limit_expensive)])
def generate_document(case_id: str, request: DocumentGenerateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Generate a document (e.g. RTI draft) for this case."""
    return document_service.generate_case_document(db, case_id, current_user.id, request)

@router.get("/{case_id}/documents", response_model=list[DocumentResponse])
def get_documents(case_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all generated documents for a case."""
    case = case_service.get_case(db, case_id, current_user.id)
    return [DocumentResponse.model_validate(doc) for doc in case.documents]

@router.get("/{case_id}/documents/{document_id}", response_model=DocumentResponse)
def get_document(case_id: str, document_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a specific generated document by ID."""
    doc = document_service.get_document(db, case_id, document_id, current_user.id)
    return DocumentResponse.model_validate(doc)

@router.get("/{case_id}/documents/{document_id}/pdf")
def get_document_pdf(case_id: str, document_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Download a generated document as PDF."""
    doc = document_service.get_document(db, case_id, document_id, current_user.id)
    
    if not doc.content:
        raise HTTPException(status_code=400, detail="Document has no text content to render as PDF")
        
    from utils.pdf_generator import generate_pdf_bytes
    try:
        pdf_bytes = generate_pdf_bytes(doc.content)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={doc.document_type}_Application_{doc.version}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@router.post("/{case_id}/file", response_model=FilingResponse)
def file_case(case_id: str, request: FilingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Record that the citizen has filed the RTI."""
    return filing_service.file_case(db, case_id, current_user.id, request)

@router.get("/{case_id}/timeline", response_model=CaseTimelineResponse)
def get_case_timeline(case_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get the full timeline for a filed case."""
    return filing_service.get_case_timeline(db, case_id, current_user.id)

from fastapi import UploadFile, File
@router.post("/{case_id}/responses", response_model=ResponseAnalysisResponse, dependencies=[Depends(rate_limit_expensive)])
async def upload_and_analyze_response(case_id: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Upload a government response PDF, extract text, and analyze it against the RTI."""
    return await response_service.upload_and_analyze_response(db, case_id, current_user.id, file)

@router.post("/{case_id}/confirm-appeal", response_model=AppealResponse)
def confirm_appeal(case_id: str, confirmation: AppealConfirmRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services import appeal_service
    return appeal_service.confirm_appeal(db, case_id, current_user.id, confirmation)

@router.get("/{case_id}/appeals", response_model=list[AppealResponse])
def get_appeals(case_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services import appeal_service
    return appeal_service.get_appeals(db, case_id, current_user.id)

@router.post("/{case_id}/appeals/{appeal_id}/resolve-authority", response_model=AppealResponse)
def resolve_appeal_authority(case_id: str, appeal_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services import appeal_authority_service
    return appeal_authority_service.resolve_appellate_authority(db, case_id, appeal_id, current_user.id)

@router.post("/{case_id}/appeals/{appeal_id}/generate-document", response_model=DocumentResponse, dependencies=[Depends(rate_limit_expensive)])
def generate_appeal_document(case_id: str, appeal_id: str, request: dict = {}, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services import appeal_service
    lang = request.get("language", "english")
    return appeal_service.generate_appeal_document(db, case_id, appeal_id, current_user.id, lang)
    
@router.post("/{case_id}/appeals/{appeal_id}/quality-check")
def quality_check_appeal(case_id: str, appeal_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services import appeal_service
    return appeal_service.quality_check_appeal(db, case_id, appeal_id, current_user.id)

@router.post("/{case_id}/appeals/{appeal_id}/file", response_model=FilingResponse)
def file_appeal(case_id: str, appeal_id: str, request: FilingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services import appeal_service
    return appeal_service.file_appeal(db, case_id, appeal_id, current_user.id, request)

@router.post("/import", response_model=CaseResponse)
def import_legacy_case(legacy_data: TrackerImport, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Import a case from the legacy browser localStorage tracker."""
    return case_service.import_legacy_tracker(db, current_user.id, legacy_data.model_dump())
