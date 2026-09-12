from pydantic import BaseModel


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    chunk_count: int