from fastmcp import FastMCP

# FastMCP 인스턴스 생성
mcp = FastMCP()

@mcp.tool
def hello_tool() -> str:
    add_tool.enable()
    return "Hello!"

@mcp.tool(enabled=False)
def add_tool(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

mcp.run(
    transport="http",
    host="0.0.0.0",
    port=9000,
)