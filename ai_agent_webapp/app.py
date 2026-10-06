import os
import requests

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver


load_dotenv(override=True)


DB_URI = os.getenv("SUPABASE_DB_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not DB_URI:
    raise ValueError("SUPABASE_DB_URI is missing")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")


# -------------------------
# TOOL
# -------------------------

def get_weather(city: str):
    """Get current weather for a given city."""

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
        "city": city,
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"]
    }


# -------------------------
# LLM
# -------------------------

llm = ChatOpenAI(
    model="gpt-5-mini",
    api_key=OPENAI_API_KEY,
    temperature=0
)


system_prompt = """
You are a helpful weather AI assistant.

When the user asks about weather,
always use the get_weather tool.

Use previous conversation context when useful.

Keep answers clear and concise.
"""


# -------------------------
# DATABASE + AGENT
# -------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:

        checkpointer.setup()

        agent = create_agent(
            model=llm,
            tools=[get_weather],
            system_prompt=system_prompt,
            checkpointer=checkpointer
        )

        app.state.agent = agent

        print("Weather AI Agent started.")

        yield

        print("Weather AI Agent stopped.")


# -------------------------
# FASTAPI
# -------------------------

app = FastAPI(
    title="Weather AI Agent",
    description="AI weather assistant built with FastAPI, LangChain and LangGraph.",
    version="1.0.0",
    lifespan=lifespan
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


templates = Jinja2Templates(
    directory="templates"
)


# -------------------------
# REQUEST MODEL
# -------------------------

class ChatRequest(BaseModel):
    message: str
    thread_id: str


# -------------------------
# ROUTES
# -------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "Weather AI Agent"
    }


@app.post("/chat")
def chat(data: ChatRequest, request: Request):

    try:

        agent = request.app.state.agent

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": data.message
                    }
                ]
            },
            {
                "configurable": {
                    "thread_id": data.thread_id
                }
            }
        )

        answer = response["messages"][-1].content

        return {
            "answer": answer
        }

    except Exception as error:

        print("ERROR:", error)

        return {
            "answer": "Something went wrong. Please try again."
        }