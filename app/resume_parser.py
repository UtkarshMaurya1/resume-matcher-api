from pdfminer.high_level import extract_text as extract_pdf_text
import docx

def parse_pdf(path: str) -> str:
    return extract_pdf_text(path)

def parse_docx(path: str) -> str:
    doc = docx.Document(path)
    return "/n".join([p.text for p in doc.paragraphs])

def parse_resume(file_path: str) -> str:
    if file_path.lower().endswith('pdf'):
        return parse_pdf(file_path)
    elif file_path.lower().endswith('docx'):
        return parse_docx(file_path)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()