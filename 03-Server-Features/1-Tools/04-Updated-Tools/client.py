from fastmcp import Client

async def message_handler(message):
    """Handle all MCP messages from the server."""
    if hasattr(message, 'root'):
        method = message.root.method
        print(f"Received: {method}")
        
        # Handle specific notifications
        if method == "notifications/tools/list_changed":
            print("Tools have changed - might want to refresh tool cache")
        elif method == "notifications/resources/list_changed":
            print("Resources have changed")


async def main():
    async with Client(
            "server.py",
            message_handler=message_handler,
        ) as client:
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        print(f"\nAvailable tools: {tool_names}")
        
        result = await client.call_tool("hello_tool")
        print(f"\nResult: {result}")
        
        # Check if tools changed after calling hello_tool
        tools_after = await client.list_tools()
        tool_names_after = [tool.name for tool in tools_after]
        print(f"\nAvailable tools after hello_tool: {tool_names_after}")
        
        result = await client.call_tool("add_tool", {"a": 5, "b": 3})
        print(f"\nResult: {result}")
        
        # Check if tools changed after calling add_tool
        tools_after2 = await client.list_tools()
        tool_names_after2 = [tool.name for tool in tools_after2]
        print(f"\nAvailable tools after add_tool: {tool_names_after2}")
        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
