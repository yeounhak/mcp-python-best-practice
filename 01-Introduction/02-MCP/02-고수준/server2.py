# ✅ 권장: FastMCP 2.0 Version ✅ 
from fastmcp import FastMCP
mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """두 수를 더합니다"""
    return a + b

if __name__ == "__main__":
    mcp.run(transport='http')