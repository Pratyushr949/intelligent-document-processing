from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

APP_NAME = "doc_test"
USER_ID = "user1"
SESSION_ID = "session1"

agent = Agent(
    name="test_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant."
)

session_service = InMemorySessionService()

session_service.create_session_sync(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)

runner = Runner(
    app_name=APP_NAME,
    agent=agent,
    session_service=session_service
)

message = types.Content(
    role="user",
    parts=[
        types.Part(text="What is the capital of India?")
    ]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=message
):
    print(event)