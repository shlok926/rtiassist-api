import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def generate_pdf_bytes(draft_text: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1 * inch,
        leftMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )
    
    styles = getSampleStyleSheet()
    
    # Create a professional style for the RTI body
    rti_style = ParagraphStyle(
        name="RTIStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        spaceAfter=10,
    )
    
    bold_style = ParagraphStyle(
        name="RTIBold",
        parent=rti_style,
        fontName="Helvetica-Bold",
    )

    story = []
    
    # Process text line by line to maintain formatting
    lines = draft_text.split('\n')
    for line in lines:
        text = line.strip()
        if not text:
            story.append(Spacer(1, 10))
            continue
            
        # Basic formatting logic for headers or subject lines
        if text.lower().startswith("subject:") or text.lower().startswith("to,") or text.lower().startswith("date:"):
            p = Paragraph(f"<b>{text}</b>", bold_style)
        else:
            p = Paragraph(text, rti_style)
            
        story.append(p)
        
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
