from langchain_ollama import ChatOllama

llama = ChatOllama(
    model="llama3.2"
)

response = llama.invoke("Hello!")
print(response.content)