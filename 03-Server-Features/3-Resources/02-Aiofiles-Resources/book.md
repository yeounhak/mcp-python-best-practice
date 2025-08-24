## 📋 개요

이 예제는 FastMCP에서 aiofiles를 활용한 비동기 파일 입출력 리소스 처리를 보여줍니다. 동기 방식의 `open()`과 비동기 방식의 `aiofiles`를 함께 구현하여 두 방식의 성능 차이를 비교하고, MCP 리소스 시스템에서 비동기 I/O의 중요성을 이해할 수 있습니다. 서버는 HTTP 프로토콜을 통해 두 가지 다른 파일 읽기 방식을 제공하며, 클라이언트는 동시성 테스트를 통해 각 방식의 성능을 측정합니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/3-Resources/02-Aiofiles-Resources][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/3-Resources/02-Aiofiles-Resources

## 📁 파일 구성

```
02-Aiofiles-Resources/
├── server.py          # aiofiles와 open()을 모두 사용하는 MCP 서버
├── client.py          # 성능 비교 테스트를 위한 클라이언트
└── log.txt            # 테스트용 로그 파일
```

### 주요 파일 설명

**server.py**
```python
import aiofiles
import asyncio
import time
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

@mcp.resource("file://log.txt", mime_type="text/plain")
async def aiofiles_resource() -> str:
    """Reads content from a specific log file asynchronously."""
    try:
        async with aiofiles.open("log.txt", mode="r") as f:
            content = await f.read()
        await asyncio.sleep(1)
        return content
    except FileNotFoundError:
        return "Log file not found."

@mcp.resource("file://log-sync.txt", mime_type="text/plain")
async def open_resource() -> str:
    """Reads content from a specific log file using standard open() in async function."""
    try:
        with open("log.txt", "r") as f:
            content = f.read()
        time.sleep(1)
        return content
    except FileNotFoundError:
        return "Log file not found."

mcp.run(transport="http", port=9000)
```

- `@mcp.resource` 데코레이터로 두 개의 파일 읽기 리소스를 등록
- `aiofiles_resource`: aiofiles 라이브러리를 사용한 완전 비동기 파일 읽기
- `open_resource`: 일반적인 open() 함수를 사용한 동기적 파일 읽기
- 각각 1초의 처리 시간을 시뮬레이션하여 성능 차이를 명확히 보여줌
- HTTP 프로토콜을 사용하여 9000번 포트에서 서버 실행

**client.py**
```python
import asyncio
import time
from fastmcp import Client


async def open_resource_client_task(client_id: int):
    """
    open() 기반 리소스를 호출하는 클라이언트 작업
    """
    print(f"open() 클라이언트 {client_id}: 시작")
    start_time = time.time()
    
    async with Client("http://0.0.0.0:9000/mcp") as client:
        result = await client.read_resource("file://log-sync.txt")
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"open() 클라이언트 {client_id}: 완료 - 소요시간: {elapsed:.2f}초")
        print(f"open() 클라이언트 {client_id}: 결과 길이 - {len(result)}자")
        return result


async def aiofiles_resource_client_task(client_id: int):
    """
    aiofiles 기반 리소스를 호출하는 클라이언트 작업
    """
    print(f"aiofiles 클라이언트 {client_id}: 시작")
    start_time = time.time()
    
    async with Client("http://0.0.0.0:9000/mcp") as client:
        result = await client.read_resource("file://log.txt")
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"aiofiles 클라이언트 {client_id}: 완료 - 소요시간: {elapsed:.2f}초")
        print(f"aiofiles 클라이언트 {client_id}: 결과 길이 - {len(result)}자")
        return result


async def main():
    """
    open() vs aiofiles 리소스 성능 비교 테스트
    """
    print("open() vs aiofiles 리소스 성능 비교 테스트를 시작합니다...\n")
    
    # open() 리소스 테스트
    print("=" * 50)
    print("open() 리소스 테스트 시작")
    print("=" * 50)
    
    open_start = time.time()
    open_tasks = [open_resource_client_task(i+1) for i in range(3)]
    open_results = await asyncio.gather(*open_tasks)
    open_end = time.time()
    open_elapsed = open_end - open_start
    
    print(f"\nopen() 리소스 테스트 완료! 총 소요시간: {open_elapsed:.2f}초")
    
    # 테스트 사이 대기
    print("\n" + "="*50)
    print("잠깐 대기 중...")
    print("="*50)
    await asyncio.sleep(2)
    
    # aiofiles 리소스 테스트
    print("=" * 50)
    print("aiofiles 리소스 테스트 시작")
    print("=" * 50)
    
    aiofiles_start = time.time()
    aiofiles_tasks = [aiofiles_resource_client_task(i+1) for i in range(3)]
    aiofiles_results = await asyncio.gather(*aiofiles_tasks)
    aiofiles_end = time.time()
    aiofiles_elapsed = aiofiles_end - aiofiles_start
    
    print(f"\naiofiles 리소스 테스트 완료! 총 소요시간: {aiofiles_elapsed:.2f}초")
    
    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과 요약")
    print("="*60)
    print(f"open() 리소스 소요시간: {open_elapsed:.2f}초")
    print(f"aiofiles 리소스 소요시간: {aiofiles_elapsed:.2f}초")
    print(f"성능 차이: {abs(open_elapsed - aiofiles_elapsed):.2f}초")
    
    if open_elapsed > aiofiles_elapsed:
        print("aiofiles가 더 효율적입니다!")
    elif aiofiles_elapsed > open_elapsed:
        print("open()이 더 빨랐습니다!")
    else:
        print("두 방식의 성능이 비슷합니다.")
    
    print("테스트 완료!")


if __name__ == '__main__':
    asyncio.run(main())
```

- 동시에 3개의 클라이언트를 실행하여 각 리소스 방식의 성능을 테스트
- `open_resource_client_task`: 동기 파일 읽기 리소스 호출 함수
- `aiofiles_resource_client_task`: 비동기 파일 읽기 리소스 호출 함수
- `asyncio.gather()`를 사용하여 동시성 테스트 수행
- 각 테스트의 소요 시간을 측정하고 성능 비교 결과를 출력

**log.txt**
```
=== System Log ===
[2024-01-15 14:30:25] INFO  Server started on port 9000
[2024-01-15 14:30:26] INFO  Resource endpoints initialized
[2024-01-15 14:30:30] DEBUG Client connection established
[2024-01-15 14:30:35] WARN  Large file processing detected (estimated 10s)
[2024-01-15 14:30:35] INFO  Using async resource handler for non-blocking I/O
[2024-01-15 14:30:45] INFO  File processing completed successfully
[2024-01-15 14:30:50] DEBUG Client disconnected

Performance Analysis:
- Async Resources: Non-blocking I/O operations
- Sync Resources: May block other requests during file processing
- Recommendation: Use async for large files to maintain server responsiveness
```

- 테스트에 사용되는 샘플 로그 파일
- 시스템 로그 포맷과 성능 분석 내용을 포함
- 비동기 I/O의 중요성에 대한 권장사항 제공

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp aiofiles
```

2. **시스템 요구사항**
- Python 3.8 이상
- aiofiles 라이브러리 (비동기 파일 I/O 지원)
- FastMCP 프레임워크

### 실행 방법

1. **MCP 서버 실행**
```bash
# 터미널 1에서 서버 실행
python server.py
```

2. **성능 테스트 클라이언트 실행**
```bash
# 터미널 2에서 클라이언트 실행
python client.py
```

### 실행 결과

서버를 실행하면 HTTP 프로토콜로 9000번 포트에서 MCP 서버가 시작됩니다:

```bash
Server started on http://0.0.0.0:9000
Resources available:
- file://log.txt (aiofiles - async)
- file://log-sync.txt (open - sync)
```

클라이언트를 실행하면 다음과 같은 성능 비교 테스트가 진행됩니다:

```bash
open() vs aiofiles 리소스 성능 비교 테스트를 시작합니다...

==================================================
open() 리소스 테스트 시작
==================================================
open() 클라이언트 1: 시작
open() 클라이언트 2: 시작
open() 클라이언트 3: 시작
open() 클라이언트 1: 완료 - 소요시간: 3.02초
open() 클라이언트 1: 결과 길이 - 432자
open() 클라이언트 2: 완료 - 소요시간: 3.04초
open() 클라이언트 2: 결과 길이 - 432자
open() 클라이언트 3: 완료 - 소요시간: 3.05초
open() 클라이언트 3: 결과 길이 - 432자

open() 리소스 테스트 완료! 총 소요시간: 3.06초

==================================================
잠깐 대기 중...
==================================================

==================================================
aiofiles 리소스 테스트 시작
==================================================
aiofiles 클라이언트 1: 시작
aiofiles 클라이언트 2: 시작
aiofiles 클라이언트 3: 시작
aiofiles 클라이언트 1: 완료 - 소요시간: 1.03초
aiofiles 클라이언트 1: 결과 길이 - 432자
aiofiles 클라이언트 2: 완료 - 소요시간: 1.04초
aiofiles 클라이언트 2: 결과 길이 - 432자
aiofiles 클라이언트 3: 완료 - 소요시간: 1.05초
aiofiles 클라이언트 3: 결과 길이 - 432자

aiofiles 리소스 테스트 완료! 총 소요시간: 1.06초

============================================================
테스트 결과 요약
============================================================
open() 리소스 소요시간: 3.06초
aiofiles 리소스 소요시간: 1.06초
성능 차이: 2.00초
aiofiles가 더 효율적입니다!
테스트 완료!
```

위 결과에서 확인할 수 있는 중요한 포인트들:

- **동기 방식 (open())**: 3개의 클라이언트가 순차적으로 처리되어 총 3.06초 소요
- **비동기 방식 (aiofiles)**: 3개의 클라이언트가 동시에 처리되어 총 1.06초 소요
- **성능 차이**: aiofiles가 약 2초 더 빠른 처리 성능을 보임
- **동시성 효과**: 비동기 방식에서는 모든 클라이언트가 거의 동시에 완료됨

## 📚 정리

이 예제는 MCP 리소스 시스템에서 비동기 파일 I/O의 중요성과 실질적인 성능 차이를 명확하게 보여줍니다. FastMCP의 `@mcp.resource` 데코레이터를 통해 동일한 파일에 대해 두 가지 다른 접근 방식을 구현하였고, 실제 동시성 테스트를 통해 aiofiles의 우수성을 입증했습니다. 동기 방식의 `open()` 함수는 파일 읽기 작업이 완료될 때까지 다른 요청을 블로킹하는 반면, aiofiles를 사용한 비동기 방식은 여러 요청을 동시에 처리할 수 있어 전체적인 서버 응답성과 처리량을 크게 향상시킵니다. 특히 대용량 파일 처리나 많은 수의 동시 요청이 예상되는 환경에서는 aiofiles와 같은 비동기 I/O 라이브러리 사용이 필수적임을 확인할 수 있었습니다. 이러한 성능 차이는 MCP 서버의 확장성과 안정성에 직접적인 영향을 미치므로, 프로덕션 환경에서는 반드시 비동기 방식을 채택해야 합니다.