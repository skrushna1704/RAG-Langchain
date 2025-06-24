from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from dotenv import load_dotenv
from rag_service import RAGService

load_dotenv()

app = FastAPI(title="RAG API", description="Retrieval-Augmented Generation API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()

class QuestionRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None

class DocumentInfo(BaseModel):
    id: str
    filename: str
    content_preview: str
    chunk_count: int
    upload_date: str

@app.get("/")
async def root():
    return {"message": "RAG API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RAG API"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document for RAG"""
    try:
        # Validate file type
        allowed_extensions = ['.txt', '.pdf', '.docx', '.md']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_extension} not supported. Allowed: {allowed_extensions}"
            )
        
        # Process document
        result = await rag_service.process_document(file)
        
        return JSONResponse(content={
            "message": "Document processed successfully",
            "document_id": result["document_id"],
            "filename": file.filename,
            "chunks_created": result["chunk_count"],
            "processing_time": result["processing_time"]
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question using RAG"""
    try:
        result = await rag_service.ask_question(
            question=request.question,
            document_ids=request.document_ids
        )
        
        return JSONResponse(content={
            "answer": result["answer"],
            "sources": result["sources"],
            "confidence_score": result["confidence_score"],
            "processing_time": result["processing_time"]
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_documents():
    """Get list of uploaded documents"""
    try:
        documents = await rag_service.get_documents()
        return JSONResponse(content={"documents": documents})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its embeddings"""
    try:
        await rag_service.delete_document(document_id)
        return JSONResponse(content={"message": "Document deleted successfully"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get RAG system statistics"""
    try:
        stats = await rag_service.get_stats()
        return JSONResponse(content=stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 