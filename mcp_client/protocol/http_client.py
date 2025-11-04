import uuid
import requests
import json

from mcp_client.utils import check_url, parse_list_tools_http

class HTTPClient:
    def __init__(self, url:str):
        self.url = check_url(url)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        self.session_id = None
        self._connected = False

    def send_request(self, method: str, params: dict = None):
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method
        }
        if params is not None:
            payload["params"] = params

        url = self.url
        if self.session_id:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}session_id={self.session_id}"

        headers = dict(self.headers)
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        r = requests.post(url, headers=headers, json=payload)

        try:
            data = r.json()
        except Exception:
            data = {"error": "invalid JSON", "body": r.text}

        if not self.session_id:
            self.session_id = (
                data.get("result", {}).get("session", {}).get("id")
                or r.headers.get("mcp-session-id")
            )

        return r.status_code, data

    def connect(self) -> bool:
        try:
            params = {
                "clientInfo": {"name": "python-http-client", "version": "0.1.0"},
                "protocolVersion": "2024-11-05",
                "capabilities": {}
            }
            status, data = self.send_request("initialize", params)

            if status == 200 and "result" in data:
                self._connected = True
                return True
            
            return False
            
        except Exception as error:
            return False

    def list_tools(self) -> dict:
        if not self._connected:
            return {"error": f"Connection to the MCP server {self.url} failed"}
        
        status, data = self.send_request("tools/list")

        if "result" in data and "tools" in data["result"]:
            return parse_list_tools_http(data)
        else:
            return {"message": "Empty list tools"}

    def call_tool(self, tool_name: str, args: dict = {}) -> dict:
        if not self._connected:
            return {"error": f"Connection to the MCP server {self.url} failed"}
        
        params = {"name": tool_name, "arguments": args}
        status, data = self.send_request("tools/call", params)
        
        return data

    def close(self):
        self._connected = False