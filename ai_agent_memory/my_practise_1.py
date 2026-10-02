from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)

my_memory={}

def save_name(name:str):
    """Save name and say to user that you saved it"""
    my_memory["name"]=name
    return f"I saved your name {name}"

def get_name():
    """Get saved user name."""

    name = my_memory.get("name")

    if name:
        return f"Your name is {name}"

    return "I don't know your name"

def get_weather(city:str):
    """Get weather to user from city"""
    return "The weather in Madrid is 20 degree"

agent = create_agent(
    model=llm,
    tools=[save_name,get_name,get_weather],
    system_prompt="""
    You are a helpful assistant.

    When user tells their name,
    use save_name tool.

    When user asks about their name,
    use get_name tool.
    
    When user asks about weather use get_weather tool.
    """,
    checkpointer=InMemorySaver()
)

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
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
        {
            "configurable": {
                "thread_id": "1"
            }
        }
    )

    print("AI:", response["messages"][-1].content)