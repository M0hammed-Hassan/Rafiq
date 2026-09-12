import io
import os
from pypdf import PdfReader
from app.config.settings import DOCS_DIR, SUPPORTED_DOC_EXTENSIONS


def _read_text_file(path: str) -> str:
    with open(path, "r",  encoding="utf-8") as f:
        return f.read()

def _read_pdf_file(path: str) -> str:
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages).strip()

def load_documents() -> list[dict]:
    """
    This function for reading every .md / .txt / .pdf file in the data/docs.
    """
    documents = []

    if not os.path.isdir(DOCS_DIR):
        return documents

    for filename in sorted(os.listdir(DOCS_DIR)):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in SUPPORTED_DOC_EXTENSIONS:
            continue

        path = os.path.join(DOCS_DIR, filename)

        if ext == ".pdf":
            text = _read_pdf_file(path)
        else:
            text = _read_text_file(path)

        if not text.strip():
            print(f"{filename} produced no extractable text")
            continue

        documents.append(
            {
                "source":filename, 
                "text":text
            }
        )

    return documents


def _extract_text(filename:str, content:bytes):
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(io.BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages).strip()

    return content.decode("utf-8").strip()

def extract_uploaded_document(filename: str, content:bytes) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_DOC_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {ext} -- Supported types only: {SUPPORTED_DOC_EXTENSIONS}"
        )
    text = _extract_text(filename, content)

    if not text:
        raise ValueError("No extractable text found in this file")

    return text
    