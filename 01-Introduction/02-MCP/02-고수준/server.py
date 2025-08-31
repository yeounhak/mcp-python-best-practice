from mcp.server.fastmcp import FastMCP
mcp = FastMCP()

@mcp.tool()
def add(a: int, b: int) -> int:
    """두 수를 더합니다"""
    return a + b

if __name__ == "__main__":
    mcp.run(transport='sse')