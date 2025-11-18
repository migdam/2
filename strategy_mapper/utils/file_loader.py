import os
from PyPDF2 import PdfReader
from docx import Document

def load_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return load_pdf(path)
    elif ext == ".docx":
        return load_docx(path)
    elif ext == ".txt":
        return load_txt(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        try:
            text.append(page.extract_text() or "")
        except:
            continue
    return "\n".join(text)

def load_docx(path: str) -> str:
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)

def load_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()
