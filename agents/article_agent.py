from gemini_model import llm
from utils.utils import get_text_content, get_last_ai_message

from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

system_prompt = """
    Kamu adalah AI Agent yang bisa membaca dan memahami berita dari file tertentu.
"""

@tool
def read_article(path: str):
    """Use this when user asks to read an article"""
    
    vault = "/home/fakhry/dev/obsidian/news"
    return vault

def create_news_agent():
    """Create and return a configured news agent."""
    
    load_dotenv()

    return create_agent(
        model=llm,
        tools=[get_latest_news],
        system_prompt=system_prompt,
        checkpointer=InMemorySaver()
    )

def run_news_agent():
    print("=== Running News Agent ===")
    agent = create_news_agent()
    config = {"configurable": {"thread_id": "1"}}

    while True:
        user_message = input("User message: ")
        response = agent.invoke(
            {"messages": HumanMessage(content=user_message)},
            config
        )
        ai_message = get_last_ai_message(response['messages'])

        print(get_text_content(ai_message))
        print()
