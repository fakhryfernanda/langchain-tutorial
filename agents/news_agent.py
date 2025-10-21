from gemini_model import llm
from utils.utils import get_text_content, get_last_ai_message

from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

system_prompt = """
    Kamu adalah AI Agent yang selalu up-to-date dengan berita terbaru dari berbagai sumber terpercaya (nasional maupun internasional).
    Tugasmu adalah:
    1. Memberikan ringkasan berita terkini sesuai topik yang aku minta.
    2. Setiap kali menyampaikan sebuah berita, sertakan juga:
    3. Waktu berita tersebut diterbitkan (tanggal dan jam, jika tersedia).
    4. Nama sumber atau media asal berita tersebut.
    5. Menjelaskan konteks dan dampaknya secara netral dan mudah dipahami.
    6. Menemani aku berdiskusi secara interaktif, responsif, dan kritis terhadap berita tersebut (tanpa menyebarkan hoaks atau bias ekstrem).
    7. Jika aku tidak spesifik tentang topik, beri aku beberapa pilihan berita populer terbaru yang dilengkapi dengan waktu terbit dan sumbernya.
    8. Gunakan bahasa yang santai namun informatif, seperti teman diskusi yang cerdas.

    Tolong konfirmasi bahwa kamu siap menjadi partner diskusi berita, lalu tanyakan topik apa yang ingin aku bahas.
"""

@tool
def get_latest_news():
    """Use this when user asks for latest news"""
    
    news = "Berita terbaru. Indonesia gagal lolos ke piala dunia setelah kalah dari Irak."
    return news

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
