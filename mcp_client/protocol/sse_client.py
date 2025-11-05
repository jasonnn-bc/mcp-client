import asyncio
from typing import Optional, Dict, Any, List
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.types import CallToolResult, TextContent

from mcp_client.utils import parse_list_tools, parse_call_tool

class SSEClient:
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self._connected = False

    async def connect(self, server_url:str) -> bool:
        try:
            streams = await self.exit_stack.enter_async_context(
                sse_client(url=server_url)
            )
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(*streams)
            )
            await self.session.initialize()
            self._connected = True
            return True
        except Exception as error:
            return False

    async def list_tools(self, parse:bool=False) -> List[Dict[str, Any]]:
        if not self._connected or not self.session:
            raise RuntimeError("Not connected. Call connect() first")
        
        try:
            result = await self.session.list_tools()
            return parse_list_tools(result) if parse else result
        except Exception as e:
            raise

    async def call_tool(
            self, tool_name: str, arguments: Dict[str, Any] = {}, parse:bool=False
            ) -> dict or CallToolResult:
        if not self._connected or not self.session:
            raise RuntimeError("Not connected. Call connect() first")
        
        try:
            result = await self.session.call_tool(tool_name, arguments)
            return result if not parse else parse_call_tool(result)
            
        except Exception as e:
            return self.handle_call_tool_error(f"{e}", error=True)

    def handle_call_tool_error(self, content:str, error:bool) -> CallToolResult:
        return CallToolResult(
            content=[TextContent(type='text', text=content)],
            isError=error
        )
        
    async def close(self):
        try:
            await self.exit_stack.aclose()
            self._connected = False
        except Exception as e:
            pass

    def is_connected(self) -> bool:
        return self._connected