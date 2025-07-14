from datetime import datetime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

from agents.tasks import task_agent
from agents.news import news_agent
from agents.weather import weather_agent
from agents.mailer import mailer_agent

load_dotenv()

async def main() -> None:
    date = datetime.now()
    formattedDate = date.strftime("%A, %B %d, %Y at %I:%M %p")
    weather_summary = await weather_agent.run(task=f"Summarize the weather in Bedford, Loretto, and State College for today, {formattedDate}, please. Be sure to include times of precipitation where applicable.")
    task_summary = await task_agent.run(task=f"Outline my todo tasks please.")
    news_summary = await news_agent.run(task=f"Summarize the news for today, {formattedDate}, please.")
    await mailer_agent.run(task=f"Please send my morning report. Use the date, {formattedDate}, and following pieces of data to create the subject and body: Weather - {weather_summary}, News - {news_summary}, Tasks - {task_summary}")

if __name__ == "__main__":
    main()