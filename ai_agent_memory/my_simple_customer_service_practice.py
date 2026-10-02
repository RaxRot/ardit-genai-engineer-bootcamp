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

orders = {
    "123": "Shipped",
    "456": "Delivered",
    "789": "Processing"
}

faq = {
    "delivery": "Delivery takes 2-3 days",
    "return": "You can return items within 30 days"
}

def save_customer(name: str):
    """Use this to save a customer."""
    my_memory["name"]=name
    return f"Nice to meet you customer {name}. I will remember you)"

def get_customer():
    """Use this to get a customer."""
    return my_memory.get("name","I do not know your name,i will call you alba)")

def check_order(order_id: str):
    """Use this to check the order."""
    return orders.get(order_id,"I do not know.Sorry")

def get_faq(question: str):
    """Use this to get a faq."""
    return faq.get(question,"Sorry, I do not know this information")

my_system_prompt="""
You are shop assistant.
If user tell his name use save_customer tool.
If user ask his name use get_customer tool.
If user ask to check order use check_order tool.
If user ask help or question about shop,delivery,return faq shop questions use get_faq tool.
If user speak something another- just be his assistant
"""

agent=create_agent(
    model=llm,
    tools=[save_customer,get_customer,check_order,get_faq],
    system_prompt=my_system_prompt,
    checkpointer=InMemorySaver()
)

while True:
    user_input = input("Ask me: ")

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