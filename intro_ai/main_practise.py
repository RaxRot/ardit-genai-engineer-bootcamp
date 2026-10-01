import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model_g="gemini-3-flash-preview"
model_provider_g="google-genai"

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

model=init_chat_model(model=model_g,model_provider=model_provider_g,api_key=GOOGLE_API_KEY)

with open("menu.txt") as f:
    menu=f.readlines()

result= model.invoke(f"With 15$ what can i buy? from menu ${menu}")

print(result.content[0]['text'])