from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableLambda,RunnableSequence
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model=ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt_template=ChatPromptTemplate.from_messages([
    ("system", "You are facts expert who knows facts about {animal}."),
    ("user", "Tell me {fact_count} facts")
])

format_prompt=RunnableLambda(lambda x: prompt_template.format_prompt(**x))

invoke_model=RunnableLambda(lambda x: model.invoke(x.to_messages()))

parse_output=RunnableLambda(lambda x:x.content)

chain = RunnableSequence(format_prompt, invoke_model, parse_output)


result=chain.invoke({"animal": "dog", "fact_count": 3})
print(result)