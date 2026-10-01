import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()


def get_price(product: str):
    """Get price for a given product."""
    product_prices={
        "apple":10,
        "banana":7,
        "orange":8,
        "mango":2,
    }

    return product_prices.get(product.lower(), "Product not found")

def check_in_stock(product: str):
    """Check if product is in stock."""
    product_in_stock = {
        "apple": True,
        "banana": False,
        "orange": True,
        "mango": True,
    }

    return product_in_stock.get(product.lower(), "Product not found")

def get_discount(product: str):
    """Get discount for a given product."""
    product_discount_in_percent = {
        "apple": 0,
        "banana": 0.2,
        "orange": 0.3,
        "mango": 0.4,
    }
    return product_discount_in_percent.get(product.lower(), "Product not found")


def get_delivery_price(city: str):
    """Get price for delivery for a given city."""
    delivery_prices = {
        "madrid": 100,
        "barcelona": 200,
        "paris": 300
    }

    return delivery_prices.get(city.lower(), "City not found")


def get_delivery_time(city: str):
    """Get delivery time for given city."""
    delivery_times = {
        "madrid": "1Day",
        "barcelona": "2Day",
        "paris": "3Day"
    }

    return delivery_times.get(city.lower(), "City not found")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(
    model="gpt-5.1",
    api_key=OPENAI_API_KEY,
    temperature=0
)


system_prompt = """
You are a helpful shop assistant.

When the user asks about the price of a product,
use the get_price tool.

When the user asks whether a product is in stock,
use the check_in_stock tool.

Also you must go to get_discount and check discount
and then give final price

Also if user ask about delivery price or write something about city-
go to get_delivery_price and check prie for delivery and then 
go to get_delivery_time and check days of delivery

"""

agent = create_agent(
    model=llm,
    tools=[get_price, check_in_stock,get_discount,get_delivery_price,get_delivery_time],
    system_prompt=system_prompt
)


if __name__ == "__main__":

    user_input = input("Ask me: ")

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    print(response["messages"][-1].content)