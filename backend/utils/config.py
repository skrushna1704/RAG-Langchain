from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Application configuration"""
    
    # CORS Settings
    ALLOWED_ORIGINS = ["http://localhost:3000"]
    
    # File Upload Settings
    ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.docx', '.md']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Server Settings
    HOST = "0.0.0.0"
    PORT = 8000
    
    # API Settings
    API_TITLE = "RAG API"
    API_DESCRIPTION = "Retrieval-Augmented Generation API"
    API_VERSION = "1.0.0" 