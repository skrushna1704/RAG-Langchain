from dotenv import load_dotenv  
from langchain_openai import ChatOpenAI
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
import os

load_dotenv()  # This loads the environment variable from .env

# You can add this line to confirm it's loaded:
print("Credential Path:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


PROJECT_ID = "langchain-bc5c0"
SESSION_ID = "user_session_new"
COLLECTION_NAME = "chat_history"

print(f"Connecting to Firestore in project {PROJECT_ID}...")
client = firestore.Client(project=PROJECT_ID)

print("Initializing Firestore chat Message History...")
chat_history = FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    client=client,
    collection=COLLECTION_NAME
)
print(f"Chat history initialized for session {SESSION_ID} in collection {COLLECTION_NAME}")
print(f"Current chat history: ", chat_history.messages)

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

print("Starting chat...")
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Goodbye!")
        break
    
    # Add user message to history
    chat_history.add_user_message(user_input)
    
    # Get AI response
    ai_response = model.invoke(chat_history.messages)
    
    # Add AI response to history
    chat_history.add_ai_message(ai_response.content)
    print("AI: ", ai_response.content)












