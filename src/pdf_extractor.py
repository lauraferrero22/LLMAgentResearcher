from PyPDF2 import PdfReader

class PdfTextExtractor():
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def run(self):
        pdf_reader = PdfReader(self.pdf_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
