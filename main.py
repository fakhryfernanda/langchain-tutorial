import asyncio
from agents.news_agent import run_news_agent

# Main execution function
async def main():
    run_news_agent()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")