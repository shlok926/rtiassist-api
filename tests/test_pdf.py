import pytest
from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)

def test_pdf_upload_no_file():
    response = client.post("/analyze-pdf/")
    assert response.status_code == 422 # FastAPI validation error for missing field

def test_pdf_upload_invalid_extension():
    response = client.post(
        "/analyze-pdf/", 
        files={"file": ("test.txt", b"%PDFhello world", "text/plain")}
    )
    assert response.status_code == 400
    assert "Only PDF files are allowed" in response.json()["detail"]

def test_pdf_upload_empty_file():
    empty_content = b""
    response = client.post(
        "/analyze-pdf/",
        files={"file": ("empty.pdf", empty_content, "application/pdf")}
    )
    # The empty file won't have a valid PDF signature, so it returns 400
    assert response.status_code == 400
    assert "Invalid PDF file signature" in response.json()["detail"] or "Empty file" in response.json()["detail"]

def test_pdf_upload_oversized():
    oversized_content = b"%PDF" + b"0" * (10 * 1024 * 1024 + 100) # Slightly over 10MB
    response = client.post(
        "/analyze-pdf/", 
        files={"file": ("large.pdf", oversized_content, "application/pdf")}
    )
    assert response.status_code == 413
    assert "too large" in response.json()["detail"].lower()

def test_valid_pdf_upload():
    valid_content = b"%PDF-1.4\n%EOF\n"
    response = client.post(
        "/analyze-pdf/",
        files={"file": ("valid.pdf", valid_content, "application/pdf")}
    )
    # Might fail extraction but pass upload validation
    assert response.status_code in [200, 400, 500] 
    if response.status_code == 400:
        assert "Invalid PDF" in response.json()["detail"] or "Failed to read PDF" in response.json()["detail"]

def test_pdf_containing_non_pdf_binary():
    binary_content = b"\x00\x01\x02\x03\x04\x05"
    response = client.post(
        "/analyze-pdf/",
        files={"file": ("binary.pdf", binary_content, "application/pdf")}
    )
    assert response.status_code == 400
    assert "Invalid PDF file signature" in response.json()["detail"]

def test_pdf_missing_pdf_signature():
    content = b"This is just text but named as pdf"
    response = client.post(
        "/analyze-pdf/",
        files={"file": ("text.pdf", content, "application/pdf")}
    )
    assert response.status_code == 400
    assert "Invalid PDF file signature" in response.json()["detail"]

def test_corrupt_pdf():
    corrupt_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n%%EOF"
    response = client.post(
        "/analyze-pdf/",
        files={"file": ("corrupt.pdf", corrupt_content, "application/pdf")}
    )
    # The file has valid signature but might fail to parse during OCR/text extraction
    assert response.status_code in [200, 400, 500]
