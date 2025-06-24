# RAG Demo App

This is a full-stack Retrieval-Augmented Generation (RAG) demo app with a FastAPI backend and a Next.js (React) frontend. You can upload documents, ask questions, and get answers using LLMs and semantic search.

## Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API key (for LLM and embeddings)

## Backend Setup
1. **Create a virtual environment and activate it:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key:**
   - Create a `.env` file in the `backend` folder:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
4. **Run the backend server:**
   ```bash
   uvicorn rag:app --reload
   ```
   The backend will be available at `http://localhost:8000` , also if not then try 8001

## Frontend Setup
1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```
2. **Run the frontend app:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`.

## Usage
- Go to the frontend URL in your browser.
- Upload a document (PDF or text).
- Ask questions in the chat interface.
- The backend will process your query using RAG and return an answer.

## Project Structure
```
backend/
  rag.py
  requirements.txt
  .env
  documents/
frontend/
  (Next.js app files)
```

## Troubleshooting
- Make sure your OpenAI API key is valid and set in the backend `.env` file.
- If you add new documents, re-upload or restart the backend to refresh the vector store.
- For CORS issues, ensure both frontend and backend are running on localhost.