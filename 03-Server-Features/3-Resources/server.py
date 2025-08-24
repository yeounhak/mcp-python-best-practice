from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# 문자열을 반환하는 기본 동적 리소스
@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """간단한 인사 메시지를 제공합니다."""
    return "Hello from FastMCP Resources!"

# JSON 데이터를 반환하는 리소스 (dict는 자동으로 직렬화됨)
@mcp.resource("data://config")
def get_config() -> dict:
    """JSON 형태의 애플리케이션 설정을 제공합니다."""
    return {
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "resources"],
    }

mcp.run(
    transport="http",
    host="0.0.0.0",
    port=9000,
)