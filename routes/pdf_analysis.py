from fastapi import APIRouter, UploadFile, File, HTTPException, status
from utils.pdf_analyzer import PDFAnalyzer
import os
import tempfile

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit

@router.post("/analyze-pdf/")
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")
    
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed")

    temp_path = None
    try:
        # Secure temp file creation
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, "wb") as f:
            # Check magic bytes first
            chunk = await file.read(1024 * 1024)
            if not chunk or not chunk.startswith(b'%PDF'):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid PDF file signature")
                
            total_size = len(chunk)
            f.write(chunk)
            
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large. Maximum size is 10MB.")
                f.write(chunk)
        
        if total_size == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file uploaded")

        # Analyze PDF
        analyzer = PDFAnalyzer(temp_path)
        result = analyzer.analyze()
        return result

    except HTTPException:
        raise
    except Exception as e:
        # Do not expose internal exception traces directly to client
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to analyze PDF document")
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
