from dotenv import load_dotenv
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

# Define the directory containing the text file and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "documents", "lord_of_the_rings.txt")
persistent_directory = os.path.join(current_dir, "db", "chroma_db")

# Check if the Chroma vector store already exists
if not os.path.exists(persistent_directory):
    print("Persistent directory does not exist. Initializing vector store...")

    # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )

    # Read the text content from the file
    loader = TextLoader(file_path)
    documents = loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50) 
    docs = text_splitter.split_documents(documents)

    # Display information about the split documents
    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(docs)}")
    print(f"Sample chunk:\n{docs[0].page_content}\n")

    # Create embeddings
    print("\n--- Creating embeddings ---")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )  # Update to a valid embedding model if needed
    print("\n--- Finished creating embeddings ---")

    # Create the vector store and persist it automatically
    print("\n--- Creating vector store ---")
    db = Chroma.from_documents(
        docs, embeddings, persist_directory=persistent_directory)
    print("\n--- Finished creating vector store ---")

else:
    print("Vector store already exists. Loading existing database...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

# Create a custom prompt template for better responses
prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Create the RAG chain
def create_rag_chain():
    """Create a RAG chain for question answering."""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    chain_type_kwargs = {"prompt": PROMPT}
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True
    )
    
    return qa_chain

def ask_question(question: str):
    """Ask a question and get an answer using RAG."""
    print(f"\n🔍 Question: {question}")
    print("-" * 50)
    
    try:
        qa_chain = create_rag_chain()
        result = qa_chain({"query": question})
        
        print(f"💡 Answer: {result['result']}")
        print(f"\n📚 Sources used:")
        for i, doc in enumerate(result['source_documents'], 1):
            print(f"   {i}. {doc.page_content[:200]}...")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have set your OPENAI_API_KEY environment variable.")

def demonstrate_rag():
    """Demonstrate the RAG system with Lord of the Rings questions."""
    print("🚀 Lord of the Rings RAG System")
    print("=" * 50)
    
    # Example questions
    questions = [
        "Who is the Ring-bearer?",
        "Where does Gandalf meet Frodo?",
        "What is Samwise Gamgee's role?",
        "How was the One Ring created?",
        "What happened to Bilbo Baggins?",
        "Who are the main characters in the story?"
    ]
    
    for question in questions:
        ask_question(question)

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key to use this RAG system.")
        print("You can set it by running: export OPENAI_API_KEY='your-api-key-here'")
    else:
        demonstrate_rag()



