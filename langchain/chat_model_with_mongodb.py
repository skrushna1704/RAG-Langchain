
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timezone
import os

# Load .env variables
load_dotenv()

# Securely encode credentials
username = quote_plus(os.getenv("MONGODB_USERNAME"))
password = quote_plus(os.getenv("MONGODB_PASSWORD"))

# MongoDB URI and connection
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.e3leecb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
collection = client["chat_history_db"]["chat_history"]

# Chat model
chat = ChatOpenAI(model="gpt-4", temperature=0)

# Use UTC timestamp for session ID
session_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

# Add initial system message
collection.insert_one({
    "session_id": session_id,
    "type": "system",
    "content": "You are a helpful assistant.",
    "timestamp": datetime.now(timezone.utc)
})

# Chat loop
print("Chat started. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Goodbye!")
        break

    # Save user message
    collection.insert_one({
        "session_id": session_id,
        "type": "human",
        "content": user_input,
        "timestamp": datetime.now(timezone.utc)
    })

    # Build message history
    docs = collection.find({"session_id": session_id}).sort("timestamp", 1)
    messages = []
    for doc in docs:
        if doc["type"] == "human":
            messages.append(HumanMessage(content=doc["content"]))
        elif doc["type"] == "ai":
            messages.append(AIMessage(content=doc["content"]))
        elif doc["type"] == "system":
            messages.append(SystemMessage(content=doc["content"]))

    # Get model response
    response = chat.invoke(messages)
    print("AI:", response.content)

    # Save AI response
    collection.insert_one({
        "session_id": session_id,
        "type": "ai",
        "content": response.content,
        "timestamp": datetime.now(timezone.utc)
    })
