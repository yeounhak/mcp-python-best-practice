import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

server = Server("mcp-simple-stdio")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="add",
            description="두 정수를 더합니다.",
            inputSchema={
                "type": "object",
                "required": ["a", "b"],
                "properties": {
                    "a": {"type": "integer", "description": "첫 번째 정수"},
                    "b": {"type": "integer", "description": "두 번째 정수"},
                },
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "add":

        a = arguments.get("a")
        b = arguments.get("b")
        
        result = a + b
        return [types.TextContent(type="text", text=str(result))]

async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())