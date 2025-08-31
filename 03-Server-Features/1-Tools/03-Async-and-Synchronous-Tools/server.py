"""
MCP 서버: 동기 vs 비동기 도구 예제

이 모듈은 동기와 비동기 작업의 차이점을 보여주는 MCP 서버를 구현합니다.
동기 도구는 이벤트 루프를 블록하는 반면, 비동기 도구는 스레드 풀을 사용하여
이벤트 루프 블로킹을 방지합니다.
"""

import anyio
from fastmcp import FastMCP
from time import sleep

# 상수 정의
CPU_TASK_DURATION = 1  # CPU 집약적 작업 시간 (초)

# FastMCP 인스턴스 생성
mcp = FastMCP()


def _cpu_intensive_task() -> str:
    """
    CPU 집약적인 작업을 시뮬레이션하는 헬퍼 함수
    
    Returns:
        str: 작업 완료 메시지
        
    Note:
        이 함수는 sleep()을 사용하여 CPU 집약적인 작업을 시뮬레이션합니다.
        실제 환경에서는 복잡한 계산이나 데이터 처리 작업을 의미할 수 있습니다.
    """
    # sleep(CPU_TASK_DURATION)
    c = 0
    for i in range(100000000):
        c += 1
    return f"{c}번 CPU 집약적 작업을 완료했습니다."


@mcp.tool
def sync_tool() -> str:
    print("동기 작업을 받았습니다.")
    """
    동기 방식 CPU 집약적 작업 도구
    
    Returns:
        str: 작업 완료 메시지
        
    Warning:
        이 도구는 동기적으로 실행되어 이벤트 루프를 블록할 수 있습니다.
        다른 요청들은 이 작업이 완료될 때까지 대기해야 합니다.
    """
    return _cpu_intensive_task()


@mcp.tool
async def async_tool() -> str:
    print("비동기 작업을 받았습니다.")
    """
    비동기 방식 CPU 집약적 작업 도구
    
    Returns:
        str: 작업 완료 메시지
        
    Note:
        anyio.to_thread.run_sync()를 사용하여 CPU 집약적 작업을 별도 스레드에서
        실행함으로써 이벤트 루프 블로킹을 방지합니다.
        이를 통해 다른 요청들이 동시에 처리될 수 있습니다.
    """
    return await anyio.to_thread.run_sync(_cpu_intensive_task)


def main() -> None:
    """
    MCP 서버 실행 함수
    
    HTTP 전송을 사용하여 모든 네트워크 인터페이스(0.0.0.0)의
    포트 9000에서 서버를 시작합니다.
    """
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=9000,
    )


if __name__ == "__main__":
    main()
