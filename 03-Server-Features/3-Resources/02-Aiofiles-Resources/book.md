## 📋 개요

이 예제는 FastMCP 프레임워크에서 aiofiles를 활용한 비동기 파일 리소스 처리와 일반 파일 I/O의 성능 비교를 다룹니다. MCP(Model Context Protocol) 서버에서 파일 리소스를 제공할 때 동기식 `open()`과 비동기식 `aiofiles.open()`의 차이점을 실제 성능 테스트를 통해 비교분석하며, 대용량 파일이나 다중 클라이언트 환경에서 비동기 I/O의 중요성을 학습할 수 있습니다. FastMCP의 `@mcp.resource` 데코레이터를 사용하여 파일 기반 리소스를 등록하고, HTTP 전송을 통해 클라이언트에서 이를 호출하는 방식을 구현했습니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/03/Server-Features/3-Resources/02-Aiofiles-Resources][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/03/Server-Features/3-Resources/02-Aiofiles-Resources

## 📁 파일 구성

```
02-Aiofiles-Resources/
├── server.py          # MCP 서버 (aiofiles vs open() 리소스 비교)
├── client.py          # 성능 비교 테스트 클라이언트
└── log.txt           # 테스트용 로그 파일
```

### 주요 파일 설명

**server.py**

**1. 비동기 파일 리소스 구현**
```python
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
```
- `aiofiles.open()`을 사용한 완전 비동기 파일 읽기
- `async with` 구문으로 파일 핸들 안전 관리
- `await f.read()`로 논블로킹 파일 읽기 수행
- 1초 비동기 지연 시뮬레이션으로 I/O 대기시간 모사

**2. 동기식 파일 리소스 구현**
```python
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
```
- 일반 `open()` 함수를 비동기 함수 내에서 사용
- 파일 I/O 동안 이벤트 루프가 블로킹됨
- `time.sleep(1)`로 동기식 지연 발생

**client.py**

**1. aiofiles 리소스 성능 테스트 함수**
```python
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
```
- 각 클라이언트별 독립적인 성능 측정
- `client.read_resource()`로 비동기 리소스 호출
- 시작과 종료 시간을 측정하여 정확한 응답시간 계산

**2. 동기식 리소스 성능 테스트 함수**
```python
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
```
- 동일한 구조로 동기식 리소스 성능 측정
- 결과 비교를 위해 동일한 메트릭 수집

**3. 병행 성능 비교 테스트**
```python
async def main():
    # open() 리소스 테스트
    open_start = time.time()
    open_tasks = [open_resource_client_task(i+1) for i in range(3)]
    open_results = await asyncio.gather(*open_tasks)
    open_end = time.time()
    open_elapsed = open_end - open_start
    
    # aiofiles 리소스 테스트
    aiofiles_start = time.time()
    aiofiles_tasks = [aiofiles_resource_client_task(i+1) for i in range(3)]
    aiofiles_results = await asyncio.gather(*aiofiles_tasks)
    aiofiles_end = time.time()
    aiofiles_elapsed = aiofiles_end - aiofiles_start
```
- 3개의 동시 클라이언트로 각 방식 테스트
- `asyncio.gather()`로 모든 작업을 병렬 실행
- 전체 소요시간과 개별 작업 시간을 모두 측정

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
- 서버 로그와 성능 분석 정보가 포함된 테스트용 파일
- 비동기와 동기식 I/O의 차이점에 대한 분석 내용 제공

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp aiofiles
```

2. **테스트 파일 확인**
```bash
# log.txt 파일이 프로젝트 디렉토리에 존재하는지 확인
ls -la log.txt
```

### 실행 방법

1. **MCP 서버 실행**
```bash
# 터미널 1에서 서버 시작
python server.py
```

2. **성능 비교 테스트 실행**
```bash
# 터미널 2에서 클라이언트 테스트 실행
python client.py
```

### 실행 결과

실제로 프로그램을 실행하면 다음과 같은 성능 비교 결과를 확인할 수 있습니다:

```bash
open() vs aiofiles 리소스 성능 비교 테스트를 시작합니다...

==================================================
open() 리소스 테스트 시작
==================================================
open() 클라이언트 1: 시작
open() 클라이언트 2: 시작
open() 클라이언트 3: 시작
open() 클라이언트 1: 완료 - 소요시간: 1.03초
open() 클라이언트 2: 완료 - 소요시간: 2.05초
open() 클라이언트 3: 완료 - 소요시간: 3.07초

open() 리소스 테스트 완료! 총 소요시간: 3.08초

==================================================
aiofiles 리소스 테스트 시작
==================================================
aiofiles 클라이언트 1: 시작
aiofiles 클라이언트 2: 시작
aiofiles 클라이언트 3: 시작
aiofiles 클라이언트 1: 완료 - 소요시간: 1.02초
aiofiles 클라이언트 2: 완료 - 소요시간: 1.02초
aiofiles 클라이언트 3: 완료 - 소요시간: 1.02초

aiofiles 리소스 테스트 완료! 총 소요시간: 1.03초

============================================================
테스트 결과 요약
============================================================
open() 리소스 소요시간: 3.08초
aiofiles 리소스 소요시간: 1.03초
성능 차이: 2.05초
aiofiles가 더 효율적입니다!
테스트 완료!
```

위 결과에서 확인할 수 있듯이:

- **open() 방식**: 동기식 I/O로 인해 클라이언트 요청이 순차적으로 처리되어 총 3.08초 소요
- **aiofiles 방식**: 비동기 I/O로 모든 클라이언트 요청이 병렬 처리되어 1.03초 소요
- **성능 차이**: aiofiles가 약 3배 빠른 성능을 보여주며, 다중 클라이언트 환경에서 현저한 차이 발생
- 각 클라이언트의 개별 응답시간도 aiofiles는 일관되게 1.02초를 유지하지만, open() 방식은 순서대로 1.03초, 2.05초, 3.07초로 점점 증가
- 서버 리소스 활용도와 응답성에서 비동기 I/O의 우수성을 명확히 확인

## 📚 정리

이 예제는 MCP 서버에서 파일 리소스를 다룰 때 동기식과 비동기식 I/O의 성능 차이를 실증적으로 보여줍니다. FastMCP의 `@mcp.resource` 데코레이터를 통해 동일한 파일을 다른 방식으로 접근하는 두 개의 리소스를 구현하고, 실제 성능 테스트를 통해 aiofiles의 우수성을 확인했습니다. 특히 다중 클라이언트 환경에서 동기식 `open()` 함수는 블로킹으로 인해 요청들이 순차 처리되어 전체 응답시간이 선형적으로 증가하지만, `aiofiles`는 진정한 비동기 I/O를 제공하여 모든 요청이 병렬로 처리되는 것을 확인했습니다. 이러한 성능 차이는 실제 프로덕션 환경에서 서버의 처리량과 응답성에 직접적인 영향을 미치므로, 파일 기반 리소스를 다루는 MCP 서버 개발 시 반드시 aiofiles와 같은 비동기 I/O 라이브러리를 활용해야 함을 시사합니다. 또한 `asyncio.gather()`를 통한 병렬 작업 관리와 정확한 성능 측정 방법론도 함께 학습할 수 있는 실용적인 예제입니다.