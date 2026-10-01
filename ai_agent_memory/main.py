import os
import requests

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


def get_weather(city: str):
    """Get current weather for a given city.
    Use this tool when the user asks about weather in a specific city."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        base_url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"]
    }

def get_location():
    """Get the user's current location."""
    response = requests.get("https://ipapi.co/json/",headers={"User-agent":"your-bot 0.1"})
    data = response.json()
    city=data["city"]
    country=data["country_name"]
    return f"Your city is {city}, country is {country}"


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-5.1",
    api_key=OPENAI_API_KEY,
    temperature=0
)


system_prompt = """
You are a helpful weather assistant.

When the user asks about weather in a city,
always use the get_weather tool.

When the user asks about their current location or where is he,
use the get_location tool.
"""


agent = create_agent(
    model=llm,
    tools=[get_weather, get_location],
    system_prompt=system_prompt,
    checkpointer=InMemorySaver()
)

while True:


    user_input = input("Ask me: ")

    if user_input.lower() in ["exit", "quit","bye"]:
        print("Bye!")
        break


    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        { "configurable": {"thread_id": "1"}}
    )

    print(response["messages"][-1].content)
