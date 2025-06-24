from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature=0)

chat_history = []
system_message = SystemMessage(content="You are a helpful assistant that can answer questions and help with tasks.")
chat_history.append(system_message)

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    chat_history.append(HumanMessage(content=user_input))
    response = model.invoke(chat_history)
    chat_history.append(response)
    print(f"AI: {response.content}")

# DALL-E 3 Image Generation

# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# from IPython.display import Image
# from openai import OpenAI
# import webbrowser
# import requests
# from PIL import Image as PILImage
# from io import BytesIO

# load_dotenv()  # Load environment variables

# client = OpenAI()

# # Generate image using DALL-E
# response = client.images.generate(
#     model="dall-e-3",
#     prompt="Draw a picture of a cute fuzzy cat with an umbrella",
#     size="1024x1024",
#     quality="standard",
#     n=1,
# )

# # Get the image URL
# image_url = response.data[0].url
# print("Image URL:", image_url)

# # Download and display the image
# response = requests.get(image_url)
# img = PILImage.open(BytesIO(response.content))
# img.show()  # This will open the image in your default image viewer

# # Option to open in browser
# print("\nOpening image in browser...")
# webbrowser.open(image_url)