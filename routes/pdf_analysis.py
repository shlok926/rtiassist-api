from fastapi import APIRouter, UploadFile, File
from utils.pdf_analyzer import PDFAnalyzer
import os

router = APIRouter()

@router.post("/analyze-pdf/")
def analyze_pdf(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    # Analyze PDF
    analyzer = PDFAnalyzer(temp_path)
    result = analyzer.analyze()
    # Remove temp file
    os.remove(temp_path)
    return result
