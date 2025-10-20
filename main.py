import asyncio
from mcp_example import mcp_test
from weather_agent import run_weather_agent

# Main execution function
async def main():
    run_weather_agent()

    await mcp_test()

if __name__ == "__main__":
    asyncio.run(main())