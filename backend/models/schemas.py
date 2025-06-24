from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None

class DocumentInfo(BaseModel):
    id: str
    filename: str
    content_preview: str
    chunk_count: int
    upload_date: str 