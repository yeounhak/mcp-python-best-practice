<div align="center" style="background:#fffbe6; border-radius:20px; box-shadow:0 4px 16px #eee; padding:40px 20px; margin:40px 0;">
  <span style="font-size:1.5em;">🌐</span>
  <div style="margin:10px 0 10px 0;">
    <span style="font-size:1.3em; font-weight:bold; color:#222;">
      FastMCP를 활용하여 HTTP 프로토콜 기반의 원격 MCP 서버와 클라이언트를 구현하고 </br>
      네트워크를 통한 도구 서버 통신 방법을 학습할 수 있습니다.
    </span>
  </div>
</div>

## 📋 개요

이 프로젝트는 Model Context Protocol(MCP)을 HTTP 프로토콜을 통해 원격으로 통신하는 방법을 보여주는 예제입니다. 기존의 로컬 stdio 통신 방식과 달리, 네트워크를 통해 MCP 서버와 클라이언트가 독립적으로 실행되면서 상호작용할 수 있는 구조를 구현했습니다.

서버는 FastMCP 라이브러리를 사용하여 HTTP 엔드포인트를 제공하며, 간단한 계산기 도구를 MCP 표준에 따라 노출합니다. 클라이언트는 HTTP를 통해 원격 서버에 연결하여 사용 가능한 도구 목록을 조회하고 실행할 수 있습니다.

이 구조는 마이크로서비스 아키텍처나 분산 시스템에서 MCP를 활용할 때의 기본적인 패턴을 제공하며, 서버와 클라이언트가 물리적으로 분리된 환경에서도 MCP 프로토콜을 사용할 수 있음을 보여줍니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02-Basic-MCP/02-remote-client-and-server][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02-Basic-MCP/02-remote-client-and-server

## 📁 파일 구성

```
02-remote-client-and-server/
├── server.py          # HTTP 기반 MCP 서버 구현
└── client.py          # HTTP 클라이언트 구현
```

### 주요 파일 설명

**server.py**
```python
# 02-remote-client-and-server/server.py 파일입니다.
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

mcp.run(transport="http")
```

- `transport="http"` 파라미터로 HTTP 기반 전송 방식 지정
- 8000번 포트의 `/mcp` 경로에서 MCP 서버 서비스 제공
- `add` 함수를 MCP 도구로 등록하여 원격에서 호출 가능하도록 구성

**client.py**
```python
# 02-remote-client-and-server/client.py 파일입니다.
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

- `Client("http://localhost:8000/mcp")`로 HTTP URL을 통한 원격 서버 연결
- `async with` 컨텍스트 매니저를 사용한 안전한 연결 관리
- `list_tools()` 메서드로 서버에서 제공하는 도구 목록 조회

## 🚀 실행

### 사전 요구사항

**1. Python 패키지 설치**
```bash
pip install fastmcp
```

**2. 네트워크 접근**
- 서버와 클라이언트가 HTTP 통신할 수 있는 네트워크 환경
- 기본적으로 localhost:8000 포트 사용

### 실행 방법

**1. MCP 서버 시작**
```bash
python server.py
```

**2. 별도 터미널에서 클라이언트 실행**
```bash
python client.py
```

### 실행 결과

**1. 서버 실행 시**
```bash
$ python server.py
INFO: Started server on http://0.0.0.0:8000
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

서버가 시작되면 HTTP 엔드포인트가 활성화되고 MCP 프로토콜 요청을 대기하는 상태가 됩니다.

**2. 클라이언트 실행 시**
```bash
$ python client.py
Available tools: [{'name': 'add', 'description': 'Adds two integer numbers together.', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'integer'}, 'b': {'type': 'integer'}}, 'required': ['a', 'b']}}]
```

클라이언트 실행 결과에서 확인할 수 있는 주요 정보:

**1. Tool Information**: 서버에서 제공하는 도구의 메타데이터가 표시됩니다
   - `name`: 도구 이름 ("add")
   - `description`: 도구 기능 설명
   - `inputSchema`: 입력 파라미터 스키마 정보

**2. Network Communication**: HTTP 프로토콜을 통한 성공적인 원격 통신이 이루어집니다
   - 서버는 독립적인 프로세스로 실행되며 HTTP 요청을 처리
   - 클라이언트는 네트워크를 통해 서버의 MCP 엔드포인트에 접근

**3. MCP Protocol Compliance**: 표준 MCP 응답 형식이 유지됩니다
   - JSON-RPC 2.0 기반의 MCP 메시지 교환
   - 도구 스키마 검증 및 타입 안정성 보장

## 📚 정리

이 예제는 Model Context Protocol을 HTTP 프로토콜을 통해 원격으로 사용하는 방법을 보여주는 중요한 구현 사례입니다. 기존의 stdio 기반 로컬 통신에서 벗어나 네트워크를 통한 분산 시스템 구조로 확장할 수 있는 가능성을 제시합니다. FastMCP 라이브러리의 `transport="http"` 옵션을 활용하여 복잡한 HTTP 서버 구현 없이도 MCP 프로토콜을 웹 서비스로 노출할 수 있으며, 클라이언트는 단순히 HTTP URL을 지정하는 것만으로 원격 서버에 연결할 수 있습니다. 이러한 구조는 마이크로서비스 아키텍처, 컨테이너 기반 배포, 클라우드 환경에서의 MCP 도구 서버 구축에 활용될 수 있으며, 서버와 클라이언트의 독립적인 스케일링과 배포를 가능하게 합니다. 또한 HTTP 기반 통신을 통해 방화벽 환경에서의 호환성과 로드 밸런싱, 프록시 서버 연동 등 엔터프라이즈 환경에서 요구되는 다양한 네트워크 구성 요소와의 통합도 용이해집니다.