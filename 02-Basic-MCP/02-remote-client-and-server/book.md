## 📋 개요

이 프로젝트는 Model Context Protocol(MCP)의 원격 통신 구현을 보여주는 HTTP 기반 클라이언트-서버 예제입니다. 로컬 stdio 통신과 달리, HTTP 프로토콜을 사용하여 네트워크를 통해 MCP 서버와 클라이언트가 통신하는 방법을 학습할 수 있습니다. FastMCP 라이브러리의 HTTP 전송 기능을 활용하여 분산 환경에서 MCP 도구를 제공하는 서버를 구축합니다.

주요 기술 스택:
- **FastMCP**: Model Context Protocol의 Python 구현체 (HTTP 전송 지원)
- **HTTP 통신**: RESTful API를 통한 원격 프로세스 간 통신
- **Python asyncio**: 비동기 프로그래밍을 위한 표준 라이브러리
- **네트워크 기반 아키텍처**: 클라이언트-서버 분리 구조

이 예제는 MCP 서버를 HTTP 엔드포인트로 노출하고, 원격 클라이언트가 네트워크를 통해 해당 서버의 도구를 호출하여 결과를 받아오는 분산 시스템의 기본 구조를 이해할 수 있습니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02/01/02-remote-client-and-server][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02/01/02-remote-client-and-server

## 📁 파일 구성

```
02-remote-client-and-server/
├── server.py          # HTTP 기반 MCP 서버 구현 (계산기 도구)
└── client.py          # HTTP 클라이언트 구현 (원격 서버 호출)
```

### 주요 파일 설명

**server.py**
```python
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

mcp.run(transport="http")
```

- `mcp.run(transport="http")`로 HTTP 전송 모드 설정하여 웹 서버로 실행
- 기본적으로 `localhost:8000` 포트에서 HTTP 서버 시작
- `/mcp` 엔드포인트를 통해 MCP 프로토콜 서비스 제공
- `@mcp.tool` 데코레이터로 등록된 `add` 함수가 HTTP API를 통해 호출 가능

**client.py**
```python
from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("http://localhost:8000/mcp") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

- `Client("http://localhost:8000/mcp")`로 HTTP URL을 통해 원격 MCP 서버에 연결
- 네트워크를 통한 비동기 통신으로 서버의 도구 목록 조회
- stdio 기반 로컬 통신과 동일한 클라이언트 API 사용하여 일관성 유지
- HTTP 연결 실패 시 자동 예외 처리 및 연결 정리

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp
```

2. **Python 3.7 이상 버전** (asyncio 및 HTTP 서버 지원을 위해 필요)

3. **네트워크 포트 8000 사용 가능** (방화벽 및 포트 충돌 확인)

### 실행 방법

1. **MCP 서버 시작**
```bash
python server.py
```

서버가 시작되면 다음과 같은 메시지가 출력됩니다:
```
MCP Server running on http://localhost:8000/mcp
```

2. **별도 터미널에서 클라이언트 실행**
```bash
python client.py
```

### 실행 결과

**1단계: 서버 실행 시 출력**
```bash
$ python server.py
MCP Server running on http://localhost:8000/mcp
Server started successfully. Waiting for connections...
```

**2단계: 클라이언트 실행 결과**
```bash
$ python client.py
Available tools: [{'name': 'add', 'description': 'Adds two integer numbers together.', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'integer'}, 'b': {'type': 'integer'}}, 'required': ['a', 'b']}}]
```

실행 결과 분석:

**1. 서버 측 동작**: HTTP 서버가 포트 8000에서 실행되며 MCP 엔드포인트 준비 완료
   - FastMCP가 내장 웹 서버를 시작하고 `/mcp` 경로에서 MCP 프로토콜 서비스
   - 클라이언트 요청을 대기하는 비동기 이벤트 루프 실행
   - 도구 등록 정보가 HTTP API를 통해 노출됨

**2. 클라이언트 측 동작**: HTTP 요청을 통해 원격 서버의 도구 정보 조회 성공
   - `list_tools()` 호출 시 `GET /mcp/list_tools` HTTP 요청 전송
   - 서버로부터 JSON 형태의 도구 스키마 정보 수신
   - 네트워크 지연이 있어도 비동기 처리로 안정적인 통신 유지

**3. 통신 프로토콜**: MCP over HTTP 구조로 RESTful API 패턴 따름
   - 요청/응답이 JSON 형태로 직렬화되어 HTTP 바디에 포함
   - 연결 상태 관리가 HTTP 세션 레벨에서 처리됨
   - 오류 발생 시 HTTP 상태 코드를 통한 명확한 에러 전달

## 📚 정리

이 예제는 Model Context Protocol(MCP)의 원격 통신 구현을 통해 분산 시스템에서의 MCP 활용 방법을 보여줍니다. 기존의 stdio 기반 로컬 통신에서 한 단계 발전하여, HTTP 프로토콜을 사용한 네트워크 기반 클라이언트-서버 아키텍처를 구현했습니다. FastMCP의 `transport="http"` 설정만으로 간단히 웹 서버 모드로 전환할 수 있으며, 클라이언트는 URL 기반 연결을 통해 동일한 API를 사용하여 원격 도구에 접근할 수 있습니다. 이러한 구조는 마이크로서비스 아키텍처나 분산 AI 시스템에서 매우 유용하며, 여러 클라이언트가 하나의 MCP 서버를 공유하거나, 서버를 독립적으로 스케일링할 수 있는 기반을 제공합니다. HTTP 기반 통신의 장점인 표준화된 프로토콜, 방화벽 친화성, 로드 밸런싱 지원 등이 MCP 생태계에 그대로 적용되어 실용적인 분산 컴퓨팅 환경을 구축할 수 있게 합니다.