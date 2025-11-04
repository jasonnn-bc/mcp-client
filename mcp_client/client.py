from typing import Union, Optional, Any

from requests import get

from mcp_client.protocol import SSEClient, HTTPClient

class MCPClient:
    
    def __init__(self, url:str, protocol:str=None, timeout:float=5.0):
        self.url = url
        self.timeout = timeout
        self.client: Union[SSEClient, HTTPClient, None] = None
        self.protocol = protocol # 'sse' or 'http' 
        self._is_async = False

    @staticmethod
    def _detect_protocol(url: str) -> str:
        try:
            response = get(url, timeout=3, stream=True)
            content_type = response.headers.get('Content-Type', '').lower()
            response.close()
            
            if 'text/event-stream' in content_type:
                return 'sse'
            
            if 'application/json' in content_type:
                return 'http'
            return 'http'
        except Exception as e:
            return None

    async def connect(self, protocol: str = None) -> bool:
        if not protocol:
            self.protocol = self._detect_protocol(self.url)
        else:
            self.protocol = protocol.lower()
        
        if self.protocol == 'sse':
            self.client = SSEClient()
            self._is_async = True
            success = await self.client.connect(self.url)
        elif self.protocol == 'http':
            self.client = HTTPClient(self.url)
            self._is_async = False
            success = self.client.connect()
        
        return success

    async def list_tools(self) -> list[dict[str, Any]]:
        if not self.client:
            return {"error": f"Connection to the MCP server {self.url} failed"}
        
        if self._is_async:
            return await self.client.list_tools()
        else:
            return self.client.list_tools()

    async def call_tool(self, tool_name: str, arguments: dict[str, Any] = None) -> dict[str, Any]:
        if not self.client:
            return {"error": f"Connection to the MCP server {self.url} failed"}
        
        if self._is_async:
            return await self.client.call_tool(tool_name, arguments)
        else:
            return self.client.call_tool(tool_name, arguments)

    async def close(self):
        if not self.client:
            return
        
        if self._is_async:
            await self.client.close()
        else:
            self.client.close()
        
    def get_protocol(self) -> Optional[str]:
        return self.protocol