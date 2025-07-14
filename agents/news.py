from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import requests
from dotenv import load_dotenv
import os

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.environ["OPENAI_API_KEY"],
)

async def get_news() -> str:
    """Get the today's news data in JSON format."""
    newsResponse = requests.get(f"https://api.thenewsapi.com/v1/news/top?api_token={os.environ["NEWS_API_KEY"]}&locale=us&limit=3")
    return { 
        "Raw JSON": newsResponse.json()
   }

news_agent = AssistantAgent(
    name="NewsAgent",
    model_client=model_client,
    system_message="You are a news assistant who analyzes news articles and suscinctly summarizes them.",
    reflect_on_tool_use=True,
    model_client_stream=True,
    tools= [ get_news ],
)