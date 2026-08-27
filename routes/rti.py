from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

router = APIRouter(prefix="/rti", tags=["RTI"])

@router.post("/generate")
async def generate_rti():
    raise HTTPException(
        status_code=410,
        detail="The /rti/generate endpoint is deprecated and has been permanently removed. Please migrate to the Case-based workflow (POST /cases)."
    )

class PDFRequest(BaseModel):
    draft: str

@router.post("/pdf")
async def generate_rti_pdf(request: PDFRequest):
    raise HTTPException(
        status_code=410,
        detail="The legacy /rti/pdf endpoint is deprecated. Use the Case Document PDF generation workflow."
    )
