from mcp.types import CallToolResult, Tool

def parse_list_tools(result:Tool) -> list[dict]:
    tools = []
    for tool in result.tools:
        tools.append({
            "name": tool.name,
            "description": tool.description or "",
            "input_schema": tool.inputSchema,
            "output_schema": tool.outputSchema
        })
    return tools

def parse_list_tools_http(result:dict) -> list[dict]:
    tools = []
    for tool in result["result"]["tools"]:
        output_schema = None if not "outputSchema" in tool else tool["outputSchema"]
        tools.append({
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["inputSchema"],
            "output_schema": output_schema
        })
    return tools

def parse_call_tool(result:CallToolResult) -> dict:
    return {
        "isError": result.isError,
        "content": result.content,
        "structuredContent": result.structuredContent
    }

def check_url(url:str) -> str:
    """Check if url starts with http or https"""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return f"http://{url}"