from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import ChatMessage
from langchain_anthropic import ChatAnthropic

load_dotenv()

claude = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)
result=claude.invoke("What is the capital of India?")
print(result.content)

llm = ChatOpenAI(model="gpt-4o", temperature=0)
result=llm.invoke("What is the capital of France?")
print(result.content)




# # 1. Create a new chat model
# chat_model = ChatOpenAI(model="gpt-4o", temperature=0)

# # 2. Create a new chat message
# chat_message = ChatMessage(role="user", content="What is the capital of France?")

# # 3. Invoke the chat model
# print(chat_model.invoke(chat_message))
