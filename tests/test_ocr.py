import pytest
import os
from unittest.mock import patch, MagicMock
from services.ocr_service import OCRService
from fpdf import FPDF

def create_fake_pdf(text="Native PDF text content"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=text, ln=True, align="C")
    
    # Save to a temporary file
    import tempfile
    fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    pdf.output(temp_path)
    return temp_path

def test_native_text_extraction():
    temp_path = create_fake_pdf("This is a lot of text so native extraction succeeds. " * 10)
    
    try:
        service = OCRService()
        result = service.extract_text(temp_path)
        
        assert result["method"] == "NATIVE_TEXT"
        assert result["ocr_used"] is False
        assert result["page_count"] == 1
        assert "native extraction succeeds" in result["text"].lower()
    finally:
        os.remove(temp_path)

def test_ocr_fallback_triggered():
    # An empty PDF will yield < 50 chars natively, triggering OCR fallback
    temp_path = create_fake_pdf("short")
    
    try:
        service = OCRService()
        
        # Mock pytesseract to simulate OCR succeeding
        with patch('pytesseract.image_to_string') as mock_ocr, \
             patch('pdfplumber.page.Page.to_image') as mock_to_image:
            
            mock_ocr.return_value = "Simulated OCR Extracted Text"
            
            # We mock to_image so it doesn't fail on CI if poppler/ghostscript isn't installed
            mock_img = MagicMock()
            mock_img.original = "FakeImage"
            mock_to_image.return_value = mock_img
            
            result = service.extract_text(temp_path)
            
            assert result["method"] == "OCR"
            assert result["ocr_used"] is True
            assert "Simulated OCR Extracted Text" in result["text"]
            
    finally:
        os.remove(temp_path)

def test_ocr_failure_warning():
    temp_path = create_fake_pdf("short")
    
    try:
        service = OCRService()
        
        with patch('pytesseract.image_to_string') as mock_ocr, \
             patch('pdfplumber.page.Page.to_image') as mock_to_image:
            
            mock_ocr.side_effect = Exception("OCR Engine Missing")
            
            mock_img = MagicMock()
            mock_img.original = "FakeImage"
            mock_to_image.return_value = mock_img
            
            result = service.extract_text(temp_path)
            
            assert result["method"] == "OCR"
            assert result["ocr_used"] is True
            assert result["extraction_warning"] == "OCR_REVIEW_REQUIRED"
            assert result["text"] == "" # Failed to extract
            
    finally:
        os.remove(temp_path)

def test_pdf_too_many_pages():
    pdf = FPDF()
    for _ in range(25):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Page", ln=True)
        
    import tempfile
    fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    pdf.output(temp_path)
    
    try:
        service = OCRService()
        result = service.extract_text(temp_path)
        
        # It should cap processing at 20 pages
        assert result["extraction_warning"] == "PAGE_LIMIT_REACHED"
    finally:
        os.remove(temp_path)
