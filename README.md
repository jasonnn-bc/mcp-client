# mcp-client

A simple Python MCP client that uses the **MCP protocol**, manages SSE/HTTP connections, handles `mcp-session-id` sessions, and sends JSON-RPC requests.


## 🚀 Usage

To use the MCP client in your own projects:

1. **Copy the folder** `mcp_client` into your project.
2. **Install the required packages** listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialize the MCPClient** with the url of your remote MCP server :
   ```python
    from mcp_client import MCPClient
    client = MCPClient(url="mon_serveur_mcp:8000/mcp")
    await client.connect()
   ```

## 🔧 Available Methods
1. List available tools from the MCP server :
   ```python
    tools = await client.list_tools()
   ```
2. Call a remote tool :
   ```python
    parameters = {"param_name": param_value}
    tools = await client.call_tool()
   ```
3. 🛑 Closing the connection
   ```python
    await client.close()
   ```

## 📌 Notes

- This client is designed to be lightweight and easily embeddable in your Python projects.

- It follows the MCP protocol for communication and tool invocation.