from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY =os.getenv("GOOGLE_API_KEY")
model_g="gemini-3-flash-preview"
model_provider_g="google-genai"

model=init_chat_model(
    model=model_g,
    model_provider=model_provider_g,
    api_key=GOOGLE_API_KEY)

with open("prices.txt") as file:
    prices=file.readlines()

response = model.invoke(f"Hello,how are you? What is the cheapest thing?{prices}")
print(response.content[0]['text'])