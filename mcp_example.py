from pprint import pprint
from gemini_model import llm
from mcp_client import create_mcp_client
from langchain.agents import create_agent

async def mcp_test():
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