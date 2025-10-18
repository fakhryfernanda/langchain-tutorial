import os
import json
import pprint
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Indonesian. Translate the user sentence.",
    ),
    ("human", "I love you, you love me. We are happy family."),
]
ai_msg = llm.invoke(messages)
print("Translate:", ai_msg)
print()

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
weather = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print("Weather report:")
print(weather)