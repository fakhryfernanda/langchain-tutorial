from langchain_mcp_adapters.client import MultiServerMCPClient


def create_mcp_client():
    """Create and return an MCP client with configured servers."""
    client = MultiServerMCPClient(
        {
            "calculator": {
                "transport": "stdio",
                "command": "uvx",
                "args": ["mcp-server-calculator"],
            }
        }
    )
    return client