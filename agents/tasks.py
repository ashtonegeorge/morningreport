from notion_client import Client
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.environ["OPENAI_API_KEY"],
)

def get_tasks() -> str:
    notion = Client(auth=os.environ['NOTION_KEY'])
    database_id = os.environ['NOTION_DATABASE_ID']

    response = notion.databases.query( database_id=database_id )

    tasks = []
    for result in response["results"]:
        props = result["properties"]
        tasks.append(f'Task name : {props['Task name']['title'][0]['text']['content']}, Due Date: {props['Due date']['date']}, Status: {props['Status']['status']['name']}')

    return tasks   

task_agent = AssistantAgent(
    name="TaskAgent",
    model_client=model_client,
    system_message="You are a task assistant who outlines todo-list tasks, listing them by due date descending (from nearest due to furthest due).",
    reflect_on_tool_use=True,
    model_client_stream=True,
    tools= [ get_tasks ],
)