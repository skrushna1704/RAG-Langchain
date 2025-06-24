from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.rag_service import RAGService
from models.schemas import QuestionRequest
from utils.validators import validate_file_extension, validate_file_size

router = APIRouter(prefix="/documents", tags=["Documents"])
rag_service = RAGService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document for RAG"""
    try:
        # Validate file
        validate_file_extension(file.filename)
        
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

@router.get("/")
async def get_documents():
    """Get list of uploaded documents"""
    try:
        documents = await rag_service.get_documents()
        return JSONResponse(content={"documents": documents})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its embeddings"""
    try:
        await rag_service.delete_document(document_id)
        return JSONResponse(content={"message": "Document deleted successfully"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 