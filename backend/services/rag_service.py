import os
import uuid
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import UploadFile, HTTPException
import json

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize vector store
        self.persist_directory = "vector_db"
        self.db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
        # Document metadata storage
        self.documents_file = "documents_metadata.json"
        self.documents = self._load_documents_metadata()
        
        # Custom prompt template
        self.prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Answer:"""
        
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
    
    def _load_documents_metadata(self) -> Dict[str, Any]:
        """Load document metadata from file"""
        if os.path.exists(self.documents_file):
            with open(self.documents_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_documents_metadata(self):
        """Save document metadata to file"""
        with open(self.documents_file, 'w') as f:
            json.dump(self.documents, f, indent=2)
    
    async def process_document(self, file: UploadFile) -> Dict[str, Any]:
        """Process uploaded document and create embeddings"""
        start_time = time.time()
        
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Save uploaded file temporarily
        temp_path = f"temp_{document_id}_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        try:
            # Load document based on file type
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            if file_extension == '.pdf':
                loader = PyPDFLoader(temp_path)
            elif file_extension == '.docx':
                loader = Docx2txtLoader(temp_path)
            else:  # .txt, .md
                loader = TextLoader(temp_path)
            
            documents = loader.load()
            
            # Split documents into chunks
            text_splitter = CharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separator="\n"
            )
            chunks = text_splitter.split_documents(documents)
            
            # Add metadata to chunks
            for chunk in chunks:
                chunk.metadata.update({
                    "document_id": document_id,
                    "filename": file.filename,
                    "chunk_index": chunks.index(chunk)
                })
            
            # Add to vector store
            self.db.add_documents(chunks)
            
            # Store document metadata
            self.documents[document_id] = {
                "id": document_id,
                "filename": file.filename,
                "upload_date": datetime.now().isoformat(),
                "chunk_count": len(chunks),
                "file_size": len(content),
                "content_preview": chunks[0].page_content[:200] + "..." if chunks else ""
            }
            
            self._save_documents_metadata()
            
            processing_time = time.time() - start_time
            
            return {
                "document_id": document_id,
                "chunk_count": len(chunks),
                "processing_time": round(processing_time, 2)
            }
            
        except Exception as e:
            print("UPLOAD ERROR:", e)
            raise HTTPException(status_code=500, detail=str(e))
    
    async def ask_question(self, question: str, document_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Ask a question using RAG"""
        start_time = time.time()
        
        try:
            # Create retriever
            retriever = self.db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            )
            
            # Create RAG chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": self.prompt},
                return_source_documents=True
            )
            
            # Get answer
            result = qa_chain({"query": question})
            
            # Process sources
            sources = []
            for doc in result['source_documents']:
                sources.append({
                    "content": doc.page_content,
                    "document_id": doc.metadata.get("document_id"),
                    "filename": doc.metadata.get("filename"),
                    "chunk_index": doc.metadata.get("chunk_index")
                })
            
            processing_time = time.time() - start_time
            
            return {
                "answer": result['result'],
                "sources": sources,
                "confidence_score": 0.85,  # Placeholder - could be calculated based on similarity scores
                "processing_time": round(processing_time, 2)
            }
            
        except Exception as e:
            raise Exception(f"Error processing question: {str(e)}")
    
    async def get_documents(self) -> List[Dict[str, Any]]:
        """Get list of uploaded documents"""
        return list(self.documents.values())
    
    async def delete_document(self, document_id: str):
        """Delete a document and its embeddings"""
        if document_id not in self.documents:
            raise Exception("Document not found")
        
        # Remove from vector store (this is a simplified version)
        # In production, you'd want to implement proper deletion from Chroma
        
        # Remove from metadata
        del self.documents[document_id]
        self._save_documents_metadata()
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics"""
        total_documents = len(self.documents)
        total_chunks = sum(doc["chunk_count"] for doc in self.documents.values())
        
        return {
            "total_documents": total_documents,
            "total_chunks": total_chunks,
            "vector_db_size": len(self.db.get()["ids"]) if self.db.get()["ids"] else 0,
            "system_status": "healthy"
        } 