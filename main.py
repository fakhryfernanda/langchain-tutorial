import asyncio
from agents.cooking_helper_agent import run_cooking_agent

# Main execution function
async def main():
    run_cooking_agent()

if __name__ == "__main__":
    asyncio.run(main())