import io
import os
from pathlib import Path
from loguru import logger
from pypdf import PdfReader
from typing import Callable
from app.config.settings import DOCS_DIR, SUPPORTED_DOC_EXTENSIONS



def _extract_plain_text(data: bytes) -> str:
    return data.decode("utf-8").strip()


def _extract_pdf_text(data: bytes) -> str:
    reader = PdfReader(io.BytesIO(data))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages).strip()



_EXTRACTORS: dict[str, Callable[[bytes], str]] = {
    ".pdf":_extract_pdf_text,
    ".md":_extract_plain_text,
    ".txt":_extract_plain_text
}

def load_documents() -> list[dict]:
    """
    This function for reading every .md / .txt / .pdf file in the data/docs.
    """
    docs_dir = Path(DOCS_DIR)
    documents: list[dict] = []

    if not DOCS_DIR.is_dir():
        logger.warning("Docs directory not founded: %s", docs_dir)
        return documents
    
    for path in sorted(docs_dir.iterdir()):
        if path.suffix.lower() not in SUPPORTED_DOC_EXTENSIONS:
            continue

        try:
            text = _extract_text(path.name, path.read_bytes())
        except Exception:
            logger.exception("Skipping %s: failed to extract text", path.name)
            continue

        if not text:
            logger.warning("%s produced no extractable text", path.name)
            continue

        documents.append(
            {
                "source":path.name, 
                "text":text
            }
        )
    return documents


def _extract_text(filename:str, content:bytes):
    ext = Path(filename).suffix.lower()

    extractor = _EXTRACTORS.get(ext)

    if extractor is None:
        raise ValueError(
            f"Unsupported file type: {ext} - Supported types only: {SUPPORTED_DOC_EXTENSIONS}"
        )
    
    return extractor(content)

def extract_uploaded_document(filename: str, content:bytes) -> str:

    text = _extract_text(filename, content)

    if not text:
        raise ValueError("No extractable text found in this file")
    
    return text