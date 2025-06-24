from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

model=ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt_template=ChatPromptTemplate.from_messages([
    ("system", "You are facts expert who knows facts about {animal}."),
    ("user", "Tell me {fact_count} facts")
])

chain=prompt_template | model | StrOutputParser()

result=chain.invoke({"animal": "dog", "fact_count": 3})
print(result)