from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

def get_weather(city:str):
    """Get weather for a given city.Use this when user ask about weather"""
    #return "Sunny"
    return {"condition":"Sunny","temperature":25}

def get_location():
    """Get user current location. Use it when user ask about whether
    without specifying location or city """
    return "Lisbon,Portugal"


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.7
)

system_prompt="""
You are a helpful weather assistant
"""

agent = create_agent(
    model=llm,
    tools=[get_weather,get_location],
    system_prompt=system_prompt
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "How is the weather?"
        }
    ]
})

print(response["messages"][-1].content[0]["text"])