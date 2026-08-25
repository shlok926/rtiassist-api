import pdfplumber

class PDFAnalyzer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def analyze(self):
        text = self.extract_text()
        # Example: Count words, summarize, etc.
        word_count = len(text.split())
        summary = text[:500] + "..." if len(text) > 500 else text
        return {
            "word_count": word_count,
            "summary": summary
        }

if __name__ == "__main__":
    analyzer = PDFAnalyzer("Free Legal Tools _ Draft Legal Documents Online - Peshā.pdf")
    result = analyzer.analyze()
    print("Word count:", result["word_count"])
    print("Summary:", result["summary"])
