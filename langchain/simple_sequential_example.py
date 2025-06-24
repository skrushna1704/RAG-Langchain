from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableLambda, RunnableSequence
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Initialize the model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Step 1: Extract topic from text
topic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a topic extractor. Extract the main topic from the given text."),
    ("user", "What is the main topic of this text? Answer in one word.\n\nText: {text}")
])

def extract_topic(input_dict):
    formatted_prompt = topic_prompt.format_prompt(**input_dict)
    response = model.invoke(formatted_prompt.to_messages())
    return response.content.strip()

# Step 2: Generate facts about the topic
facts_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a facts expert. Generate interesting facts about the given topic."),
    ("user", "Generate 3 interesting facts about {topic}")
])

def generate_facts(topic):
    formatted_prompt = facts_prompt.format_prompt(topic=topic)
    response = model.invoke(formatted_prompt.to_messages())
    return response.content

# Step 3: Create a summary combining topic and facts
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a content summarizer. Create a brief summary."),
    ("user", "Create a 2-sentence summary about {topic} based on these facts:\n{facts}")
])

def create_summary(inputs):
    # inputs will be a dict with 'topic' and 'facts'
    formatted_prompt = summary_prompt.format_prompt(
        topic=inputs['topic'], 
        facts=inputs['facts']
    )
    response = model.invoke(formatted_prompt.to_messages())
    return response.content

# Step 4: Combine topic and facts for summary
def combine_for_summary(inputs):
    return {
        'topic': inputs['topic'],
        'facts': inputs['facts']
    }

# Step 5: Format final output
def format_output(inputs):
    return f"""
# Analysis Results

**Topic:** {inputs['topic']}

**Facts:**
{inputs['facts']}

**Summary:**
{inputs['summary']}
"""

# Create the sequential chain
analysis_chain = RunnableSequence(
    # Step 1: Extract topic
    RunnableLambda(extract_topic),
    # Step 2: Generate facts about the topic
    RunnableLambda(generate_facts),
    # Step 3: Combine topic and facts
    RunnableLambda(combine_for_summary),
    # Step 4: Create summary
    RunnableLambda(create_summary),
    # Step 5: Format final output
    RunnableLambda(format_output)
)

# Test the chain
sample_text = """
Machine learning algorithms are becoming increasingly sophisticated, enabling computers to learn patterns 
from data without being explicitly programmed. These algorithms power everything from recommendation 
systems to autonomous vehicles, transforming industries across the globe.
"""

print("Running Simple Sequential Chain Example...")
print("=" * 50)

result = analysis_chain.invoke({"text": sample_text})
print(result) 