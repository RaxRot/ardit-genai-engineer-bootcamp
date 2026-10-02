from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

def weather(city:str):
    """When user asks about whether
    Tell him that now in Madrid is 25 degres!"""
    return ""

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[weather],
    system_prompt="You are a helpful assistant. If user asks about weather use weather",
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