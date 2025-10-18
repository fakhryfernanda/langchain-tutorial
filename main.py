import asyncio
from pprint import pprint
from weather_agent import create_weather_agent, Context
from mcp_client import create_mcp_client
from gemini_model import llm
from langchain.agents import create_agent

# Main execution function
async def main():
    print("=== Running Weather Agent Example ===")
    # Create and use the weather agent
    agent = create_weather_agent()

    # `thread_id` is a unique identifier for a given conversation.
    config = {"configurable": {"thread_id": "1"}}

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
        config=config,
        context=Context(user_id="1")
    )

    print()
    print(response['structured_response'])

    # Note that we can continue the conversation using the same `thread_id`.
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "thank you!"}]},
        config=config,
        context=Context(user_id="1")
    )

    print(response['structured_response'])
    
    print("\n=== Running MCP Client Example ===")
    # Create and use the MCP client
    client = create_mcp_client()

    tools = await client.get_tools()
    print("Available tools:")
    print(tools)

    calculator_agent = create_agent(llm, tools)
    response = await calculator_agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the square root of 1000?"}]}
    )

    print("\nCalculator agent response:")
    pprint(response)

if __name__ == "__main__":
    asyncio.run(main())