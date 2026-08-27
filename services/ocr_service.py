import pdfplumber
import pytesseract
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, pdf_path: str) -> dict:
        """
        Extracts text from a PDF, falling back to OCR if native text is insufficient.
        Returns extraction metadata.
        """
        text = ""
        page_count = 0
        ocr_used = False
        extraction_warning = None

        try:
            with pdfplumber.open(pdf_path) as pdf:
                page_count = len(pdf.pages)
                # First try native text extraction
                max_pages = min(20, len(pdf.pages))
                for i in range(max_pages):
                    page = pdf.pages[i]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if len(pdf.pages) > 20:
                    extraction_warning = "PAGE_LIMIT_REACHED"

                # Check if native extraction yielded meaningful text
                if len(text.strip()) < 50:
                    logger.info(f"Native text extraction yielded very little text for {pdf_path}. Attempting OCR fallback.")
                    text = "" # Reset text
                    ocr_used = True
                    try:
                        max_ocr_pages = min(20, len(pdf.pages))
                        for i in range(max_ocr_pages):
                            page = pdf.pages[i]
                            # Render page to PIL Image
                            img = page.to_image(resolution=300).original
                            page_text = pytesseract.image_to_string(img)
                            if page_text:
                                text += page_text + "\n"
                        if len(pdf.pages) > 20:
                            extraction_warning = "OCR_PAGE_LIMIT_REACHED"
                    except Exception as e:
                        logger.error(f"OCR failed: {str(e)}")
                        extraction_warning = "OCR_REVIEW_REQUIRED"
                        text = "" # Could not extract anything

                if not text.strip():
                    extraction_warning = "OCR_REVIEW_REQUIRED"

        except Exception as e:
            logger.error(f"Failed to process PDF {pdf_path}: {str(e)}")
            extraction_warning = "EXTRACTION_FAILED"

        return {
            "text": text.strip(),
            "method": "OCR" if ocr_used else "NATIVE_TEXT",
            "page_count": page_count,
            "ocr_used": ocr_used,
            "extraction_warning": extraction_warning
        }
