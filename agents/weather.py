from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
import requests
import os

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"],
)

async def get_weather(city: str) -> str:
    """Get the today's weather data in JSON format for a given city."""
    geocodingResponse = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},PA,1&appid={os.environ['OPENWEATHER_API_KEY']}")
    geocodingData = geocodingResponse.json()
    lat=geocodingData[0]['lat']
    lon=geocodingData[0]['lon']

    forecastResponse = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.environ['OPENWEATHER_API_KEY']}&units=imperial")
    dailyResponse = requests.get(f"http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&units=imperial&cnt=1&appid={os.environ['OPENWEATHER_API_KEY']}")
    
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