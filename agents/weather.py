from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import sys
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.getenv('OPENAI_API_KEY'),
)

async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    geocodingResponse = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},PA,1&appid={os.getenv('OPENWEATHER_API_KEY')}")
    geocodingData = geocodingResponse.json();
    lat=geocodingData[0]['lat']
    lon=geocodingData[0]['lon']

    forecastResponse = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.getenv('OPENWEATHER_API_KEY')}&units=imperial")
    dailyResponse = requests.get(f"http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&units=imperial&cnt=1&appid={os.getenv('OPENWEATHER_API_KEY')}")

    # print(geocodingResponse.json())
    print(forecastResponse.json())
    print()
    print()
    print()
    print()
    print(dailyResponse.json())

weather_agent = AssistantAgent(
    name="WeatherAgent",
    model_client=model_client,
    tools=[get_weather],
)

async def main() -> None:
    await get_weather("Bedford")

asyncio.run(main())