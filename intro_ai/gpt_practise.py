from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

gpt = ChatOpenAI(
    model="gpt-5.1",
    api_key=API_KEY
)

response = gpt.invoke("Hello!")
print(response.content)