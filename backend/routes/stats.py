from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.rag_service import RAGService

router = APIRouter(prefix="/stats", tags=["Statistics"])
rag_service = RAGService()

@router.get("/")
async def get_stats():
    """Get RAG system statistics"""
    try:
        stats = await rag_service.get_stats()
        return JSONResponse(content=stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 