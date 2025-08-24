import anyio
from fastmcp import FastMCP
from time import sleep

# 작업 시간 설정
CPU_TASK_DURATION = 1  # 초

# FastMCP 인스턴스 생성
mcp = FastMCP()

def cpu_intensive_func() -> str:
    """
    동기 방식의 CPU 집약적 작업
    주의: 이 함수는 이벤트 루프를 블록할 수 있음
    """
    sleep(CPU_TASK_DURATION)
    return f"{CPU_TASK_DURATION}초 동안 동기 작업을 완성하였습니다."


@mcp.tool
def sync_tool() -> str:
    """
    동기 방식의 CPU 집약적 작업
    주의: 이 함수는 이벤트 루프를 블록할 수 있음
    """
    return cpu_intensive_func()


@mcp.tool
async def async_tool() -> str:
    """
    비동기 방식의 CPU 집약적 작업
    anyio.to_thread를 사용하여 이벤트 루프 블로킹 방지
    """
    return await anyio.to_thread.run_sync(cpu_intensive_func)


if __name__ == "__main__":
    # MCP 서버 실행
    mcp.run(
        transport="http",
        host="0.0.0.0",  # 모든 인터페이스에 바인딩
        port=9000,       # 커스텀 포트
    )
