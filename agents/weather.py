import json
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.getenv('OPENAI_API_KEY'),
)

async def get_weather(city: str) -> str:
    """Get the today's weather data in JSON format for a given city."""
    geocodingResponse = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},PA,1&appid={os.getenv('OPENWEATHER_API_KEY')}")
    geocodingData = geocodingResponse.json();
    lat=geocodingData[0]['lat']
    lon=geocodingData[0]['lon']

    forecastResponse = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.getenv('OPENWEATHER_API_KEY')}&units=imperial")
    dailyResponse = requests.get(f"http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&units=imperial&cnt=1&appid={os.getenv('OPENWEATHER_API_KEY')}")
    
    data = {
        "forecast": forecastResponse.json(),
        "daily": dailyResponse.json()
    }

    return data

weather_agent = AssistantAgent(
    name="WeatherAgent",
    model_client=model_client,
    system_message="You are a weather assistant who analyzes weather data and suscinctly summarizes it for a given city or cities.",
    reflect_on_tool_use=True,
    model_client_stream=True,
    tools= [ get_weather ],
)

async def main() -> None:
    date = datetime.now()
    formattedDate = date.strftime("%A, %B %d, %Y at %I:%M %p")
    await Console(weather_agent.run_stream(task=f"Summarize the weather in Bedford for today, {formattedDate}, please."))
    await model_client.close()

asyncio.run(main())