import os.path
import base64
from email.mime.text import MIMEText

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from dotenv import load_dotenv
import os

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.environ["OPENAI_API_KEY"],
)

# If modifying these SCOPES, delete the token.json file.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def authenticate():
    creds = None
    # token.json stores the user's access and refresh tokens
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, 'html')
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

def send_email(subject: str, body: str) -> str:
    creds = authenticate()
    service = build("gmail", "v1", credentials=creds)

    message = create_message(
        sender="me",
        to="ashtongeorge17@gmail.com",
        subject=subject,
        message_text=body,
    )
    sent = service.users().messages().send(userId="me", body=message).execute()
    print(f"Message ID: {sent['id']}")
    return sent['id']

mailer_agent = AssistantAgent(
    name="MailerAgent",
    model_client=model_client,
    system_message="You are a mailer assistant who sends Morning Report emails. Please use HTML format with dark backgrounds, light text, and a teal/cobalt blue color scheme.",
    reflect_on_tool_use=True,
    model_client_stream=True,
    tools= [ send_email ],
)