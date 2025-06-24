# RAG API Backend

A FastAPI-based backend for a Retrieval-Augmented Generation (RAG) system.

## Project Structure

```
backend/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── models/                 # Data models and schemas
│   ├── __init__.py
│   └── schemas.py          # Pydantic models
├── routes/                 # API route handlers
│   ├── __init__.py
│   ├── health.py           # Health check endpoints
│   ├── documents.py        # Document management endpoints
│   ├── qa.py              # Question-answering endpoints
│   └── stats.py           # Statistics endpoints
├── services/               # Business logic layer
│   ├── __init__.py
│   └── rag_service.py      # Core RAG business logic
└── utils/                  # Utility functions
    ├── __init__.py
    ├── config.py           # Application configuration
    └── validators.py       # Validation utilities
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Document Management
- `POST /documents/upload` - Upload and process documents
- `GET /documents/` - List all documents
- `DELETE /documents/{document_id}` - Delete a document

### Question Answering
- `POST /qa/ask` - Ask questions using RAG

### Statistics
- `GET /stats/` - Get system statistics

## Running the Application

```bash
cd backend
python main.py
```

The server will start on `http://0.0.0.0:8000`

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Service Layer**: Business logic separated in services directory
- **Configuration Management**: Centralized configuration in `utils/config.py`
- **Validation**: Reusable validation utilities
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **CORS Support**: Configured for frontend integration
- **Async Operations**: All endpoints are async for better performance 