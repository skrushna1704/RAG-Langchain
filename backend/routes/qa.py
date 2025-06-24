from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.rag_service import RAGService
from models.schemas import QuestionRequest

router = APIRouter(prefix="/qa", tags=["Question Answering"])
rag_service = RAGService()

@router.post("/ask")
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