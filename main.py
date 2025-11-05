import asyncio

from mcp_client import MCPClient

async def main():
    # Initialize client
    client = MCPClient(url="http://localhost:5000/mcp")
    await client.connect()

    # Get available tools
    tools = await client.list_tools()
    print("Available tools :")
    print(tools)

    # Call distant tool
    parameters = {}
    tool_result = await client.call_tool("get-tools", parameters)
    print("Call tool : get-tools")
    print(tool_result)

    # Close client
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())