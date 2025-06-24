from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

template="Write a {tone} email to {company} expressing interest in the {position}, mentoring{skill} as a key strength.keep it to 4 lines max."

prompt_template = ChatPromptTemplate.from_template(template)
prompt=prompt_template.invoke({
    "tone": "friendly",
    "company": "Google",
    "position": "Software Engineer",
    "skill": "Python"
})
result=llm.invoke(prompt)   
print(result.content)


