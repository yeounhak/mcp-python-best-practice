## 📋 개요

이 프로젝트는 FastMCP 라이브러리를 사용하여 동기(synchronous)와 비동기(asynchronous) 도구의 성능 차이를 실습하고 비교할 수 있는 예제입니다. CPU 집약적인 작업을 동기와 비동기 방식으로 각각 구현하고, 다중 클라이언트 환경에서의 성능 차이를 측정하여 비동기 프로그래밍의 중요성을 학습할 수 있습니다.

주요 기술 스택으로는 FastMCP, anyio, asyncio를 활용하며, MCP 서버에서 동기/비동기 도구를 제공하고 클라이언트에서 동시에 여러 요청을 보내어 성능을 비교 분석합니다. 이를 통해 이벤트 루프 블로킹 현상과 `anyio.to_thread.run_sync()`를 활용한 블로킹 방지 기법을 실습할 수 있습니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02/01/03-Async-and-Synchronous-Tools][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02/01/03-Async-and-Synchronous-Tools

## 📁 파일 구성

```
03-Async-and-Synchronous-Tools/
├── server.py          # MCP 서버 구현 (동기/비동기 도구)
└── client.py          # 성능 비교 테스트 클라이언트
```

### 주요 파일 설명

**server.py**

**1. 모듈 문서화 및 기본 설정**
```python
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
```
- 모듈 레벨에서 상세한 문서화를 제공하여 코드의 목적과 동작 방식을 명확히 설명
- anyio를 활용하여 동기 함수를 비동기 스레드에서 실행
- FastMCP를 사용하여 MCP 서버 인스턴스 생성
- 상수로 CPU_TASK_DURATION을 정의하여 작업 시간을 1초로 설정

**2. CPU 집약적 작업 함수 및 동기 도구**
```python
def _cpu_intensive_task() -> str:
    """
    CPU 집약적인 작업을 시뮬레이션하는 헬퍼 함수
    
    Returns:
        str: 작업 완료 메시지
        
    Note:
        이 함수는 sleep()을 사용하여 CPU 집약적인 작업을 시뮬레이션합니다.
        실제 환경에서는 복잡한 계산이나 데이터 처리 작업을 의미할 수 있습니다.
    """
    sleep(CPU_TASK_DURATION)
    return f"{CPU_TASK_DURATION}초 동안 CPU 집약적 작업을 완료했습니다."

@mcp.tool
def sync_tool() -> str:
    """
    동기 방식 CPU 집약적 작업 도구
    
    Returns:
        str: 작업 완료 메시지
        
    Warning:
        이 도구는 동기적으로 실행되어 이벤트 루프를 블록할 수 있습니다.
        다른 요청들은 이 작업이 완료될 때까지 대기해야 합니다.
    """
    return _cpu_intensive_task()
```
- `_cpu_intensive_task()`는 private 함수로 설계되어 내부 구현을 캡슐화
- Google 스타일 docstring으로 상세한 함수 문서화 제공
- `sync_tool()`은 동기 방식으로 작업을 수행하므로 이벤트 루프가 블록됨
- Warning 섹션으로 블로킹 위험성을 명시적으로 경고

**3. 비동기 도구 및 서버 실행**
```python
@mcp.tool
async def async_tool() -> str:
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
```
- `async_tool()`에 상세한 docstring으로 비동기 처리 방식과 장점을 명확히 설명
- `_cpu_intensive_task` 함수 참조로 업데이트된 함수명 반영
- `main()` 함수를 별도로 분리하여 코드 구조 개선 및 테스트 용이성 향상
- 모듈 실행 시 `main()` 함수를 호출하는 표준 Python 패턴 적용

**client.py**

**1. 동기 도구 테스트 클라이언트**
```python
import asyncio
import time
from fastmcp import Client

async def sync_client_task(client_id: int):
    """
    동기 도구를 호출하는 클라이언트 작업
    """
    print(f"동기 클라이언트 {client_id}: 시작")
    start_time = time.time()
    
    async with Client("http://0.0.0.0:9000/mcp") as client:
        result = await client.call_tool("sync_tool")
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"동기 클라이언트 {client_id}: 완료 - 소요시간: {elapsed:.2f}초")
        print(f"동기 클라이언트 {client_id}: 결과 - {result}")
        return result
```
- 각 클라이언트가 동기 도구(`sync_tool`)를 호출하여 성능 측정
- `time.time()`을 활용하여 정확한 소요시간 계산
- 클라이언트별로 시작/완료 시간과 결과를 출력하여 실행 순서 확인

**2. 비동기 도구 테스트 클라이언트**
```python
async def async_client_task(client_id: int):
    """
    비동기 도구를 호출하는 클라이언트 작업
    """
    print(f"비동기 클라이언트 {client_id}: 시작")
    start_time = time.time()
    
    async with Client("http://0.0.0.0:9000/mcp") as client:
        result = await client.call_tool("async_tool")
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"비동기 클라이언트 {client_id}: 완료 - 소요시간: {elapsed:.2f}초")
        print(f"비동기 클라이언트 {client_id}: 결과 - {result}")
        return result
```
- 동일한 구조로 비동기 도구(`async_tool`)를 호출하여 성능 비교
- 동기 클라이언트와 동일한 측정 방식으로 공정한 비교 환경 구성

**3. 메인 성능 비교 테스트 함수**
```python
async def main():
    """
    동기/비동기 도구 성능 비교 테스트
    """
    print("동기/비동기 도구 성능 비교 테스트를 시작합니다...\n")
    
    # 동기 도구 테스트
    print("=" * 50)
    print("동기 도구 테스트 시작")
    print("=" * 50)
    
    sync_start = time.time()
    sync_tasks = [sync_client_task(i+1) for i in range(3)]
    sync_results = await asyncio.gather(*sync_tasks)
    sync_end = time.time()
    sync_elapsed = sync_end - sync_start
    
    print(f"\n동기 도구 테스트 완료! 총 소요시간: {sync_elapsed:.2f}초")
    
    # 비동기 도구 테스트
    async_start = time.time()
    async_tasks = [async_client_task(i+1) for i in range(3)]
    async_results = await asyncio.gather(*async_tasks)
    async_end = time.time()
    async_elapsed = async_end - async_start
    
    print(f"\n비동기 도구 테스트 완료! 총 소요시간: {async_elapsed:.2f}초")
    
    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과 요약")
    print("="*60)
    print(f"동기 도구 소요시간: {sync_elapsed:.2f}초")
    print(f"비동기 도구 소요시간: {async_elapsed:.2f}초")
    print(f"성능 차이: {abs(sync_elapsed - async_elapsed):.2f}초")
    print("테스트 완료!")
```
- 3개의 동시 클라이언트로 동기/비동기 도구를 각각 테스트
- `asyncio.gather()`를 사용하여 동시 실행하되 실제 서버 처리 방식에 따른 성능 차이 측정
- 전체 소요시간과 성능 차이를 정량적으로 비교하여 결과 출력

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp anyio
```

2. **Python 버전 확인**
- Python 3.8 이상 필요 (asyncio, anyio 지원)

### 실행 방법

1. **MCP 서버 실행**
```bash
python server.py
```

2. **새로운 터미널에서 클라이언트 테스트 실행**
```bash
python client.py
```

### 실행 결과

서버를 실행하면 다음과 같은 메시지가 출력됩니다:

```bash
FastMCP server running on http://0.0.0.0:9000
```

클라이언트를 실행하면 동기/비동기 도구의 성능 차이를 확인할 수 있습니다:

```bash
동기/비동기 도구 성능 비교 테스트를 시작합니다...

==================================================
동기 도구 테스트 시작
==================================================
동기 클라이언트 1: 시작
동기 클라이언트 2: 시작
동기 클라이언트 3: 시작
동기 클라이언트 1: 완료 - 소요시간: 1.02초
동기 클라이언트 1: 결과 - 1초 동안 CPU 집약적 작업을 완료했습니다.
동기 클라이언트 2: 완료 - 소요시간: 2.03초
동기 클라이언트 2: 결과 - 1초 동안 CPU 집약적 작업을 완료했습니다.
동기 클라이언트 3: 완료 - 소요시간: 3.04초
동기 클라이언트 3: 결과 - 1초 동안 CPU 집약적 작업을 완료했습니다.

동기 도구 테스트 완료! 총 소요시간: 3.04초

==================================================
비동기 도구 테스트 시작
==================================================
비동기 클라이언트 1: 시작
비동기 클라이언트 2: 시작
비동기 클라이언트 3: 시작
비동기 클라이언트 1: 완료 - 소요시간: 1.01초
비동기 클라이언트 1: 결과 - 1초 동안 CPU 집약적 작업을 완료했습니다.
비동기 클라이언트 2: 완료 - 소요시간: 1.01초
비동기 클라이언트 2: 결과 - 1초 동안 CPU 집약적 작업을 완료했습니다.
비동기 클라이언트 3: 완료 - 소요시간: 1.01초
비동기 클라이언트 3: 결과 - 1초 동안 CPU 집약적 작업을 완료했습니다.

비동기 도구 테스트 완료! 총 소요시간: 1.01초

============================================================
테스트 결과 요약
============================================================
동기 도구 소요시간: 3.04초
비동기 도구 소요시간: 1.01초
성능 차이: 2.03초
테스트 완료!
```

위 실행 결과에서 확인할 수 있듯이, 동기 도구는 각 요청이 순차적으로 처리되어 총 3초 이상이 소요되는 반면, 비동기 도구는 모든 요청이 동시에 처리되어 약 1초만 소요됩니다. 이는 비동기 프로그래밍이 I/O 집약적이거나 대기 시간이 있는 작업에서 얼마나 효과적인지를 명확하게 보여줍니다.

## 📚 정리

이 예제는 FastMCP 환경에서 동기와 비동기 도구의 성능 차이를 실질적으로 체험할 수 있는 실습 프로젝트입니다. 동기 방식의 `sync_tool()`은 이벤트 루프를 블록하여 다중 요청을 순차적으로 처리하는 반면, 비동기 방식의 `async_tool()`은 `anyio.to_thread.run_sync()`를 활용하여 CPU 집약적 작업을 별도 스레드에서 실행함으로써 이벤트 루프 블로킹을 방지합니다. 3개의 동시 클라이언트로 테스트한 결과, 동기 도구는 약 3초, 비동기 도구는 약 1초가 소요되어 약 3배의 성능 차이를 확인할 수 있었습니다. 이를 통해 MCP 서버 개발 시 적절한 비동기 패턴 적용의 중요성과 `anyio.to_thread` 같은 도구를 활용한 블로킹 방지 기법의 실용적 가치를 학습할 수 있습니다. 특히 다중 사용자 환경이나 높은 동시성이 요구되는 MCP 애플리케이션에서는 이러한 비동기 처리 방식이 필수적임을 실증적으로 보여주는 중요한 예제입니다.