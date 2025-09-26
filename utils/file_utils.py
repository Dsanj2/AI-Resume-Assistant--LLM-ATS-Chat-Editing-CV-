# utils/file_utils.py
import io
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(pdf_bytes):
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            return "PDF contains no extractable text. Provide a text-based PDF."
        return text
    except Exception as e:
        return f"PDF extraction failed: {str(e)}"

def extract_text_from_docx(docx_bytes):
    try:
        doc = Document(io.BytesIO(docx_bytes))
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        if not text.strip():
            return "DOCX contains no extractable text."
        return text
    except Exception as e:
        return f"DOCX extraction failed: {str(e)}"

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file.read())
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file.read())
    else:
        return "Unsupported file type. Please upload PDF or DOCX."
