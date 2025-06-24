from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/")
async def root():
    return {"message": "RAG API is running!"}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RAG API"} 