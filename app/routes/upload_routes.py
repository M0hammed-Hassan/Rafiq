import uuid
import logging
from app.dto.upload import UploadResponse
from app.core.ingestion import ingest_text
from app.config.settings import MAX_UPLOAD_MB
from fastapi import APIRouter, HTTPException, UploadFile
from app.core.document_loader import extract_uploaded_document


logger = logging.getLogger("rafiq")
router = APIRouter()

MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

@router.post("/api/upload", response_model=UploadResponse)
async def upload(file: UploadFile):
    content = await file.read()

    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413, detail=f"File is too large - limit is {MAX_UPLOAD_MB} MB"
        )

    try:
        text = extract_uploaded_document(file.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    document_id = uuid.uuid4().hex[:12]
    scope = f"session:{document_id}"

    chunk_count  = ingest_text(source=file.filename, text=text, scope=scope)
    if chunk_count == 0:
        raise HTTPException(status_code=400, detail="File produced no usable content to index")

    logger.info(
        "upload filename=%r document_id=%s chunks=%d", file.filename, document_id, chunk_count
    )
    return UploadResponse(
        document_id=document_id, filename=file.filename, chunk_count=chunk_count
    )