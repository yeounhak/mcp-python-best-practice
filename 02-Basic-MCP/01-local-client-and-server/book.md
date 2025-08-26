## 📋 개요

이 프로젝트는 Model Context Protocol(MCP)의 가장 기본적인 구현을 보여주는 로컬 클라이언트-서버 예제입니다. FastMCP 라이브러리를 사용하여 간단한 계산기 서버를 구축하고, 클라이언트가 stdio를 통해 해당 서버와 통신하는 방법을 학습할 수 있습니다.

주요 기술 스택:
- **FastMCP**: Model Context Protocol의 Python 구현체
- **Python asyncio**: 비동기 프로그래밍을 위한 표준 라이브러리
- **stdio 통신**: 프로세스 간 표준 입출력 스트림을 통한 통신

이 예제는 MCP 서버에서 도구를 등록하고, 클라이언트에서 해당 도구를 호출하여 결과를 받아오는 전체 흐름을 이해할 수 있는 최소한의 구현체입니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02/01/01-local-client-and-server][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02/01/01-local-client-and-server

## 📁 파일 구성

```
01-local-client-and-server/
├── server.py          # MCP 서버 구현 (계산기 도구)
└── client.py          # MCP 클라이언트 구현 (서버 호출)
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

mcp.run()
```

- `@mcp.tool` 데코레이터로 `add` 함수를 MCP 도구로 등록
- 두 정수를 더하는 간단한 계산 기능 제공
- 함수의 docstring이 도구 설명으로 사용됨
- 타입 힌팅을 통해 파라미터와 반환값 타입 명시

**client.py**
```python
from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print(f"\nAvailable tools: {tools}")
        
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"\nResult: {result}")
        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

- `Client("server.py")`로 로컬 서버 스크립트에 stdio를 통해 연결
- `list_tools()`로 서버에서 제공하는 도구 목록 조회
- `call_tool()`로 특정 도구를 호출하며 파라미터를 딕셔너리 형태로 전달
- `async with` 컨텍스트 매니저를 사용하여 안전한 연결 관리

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp
```

2. **Python 3.7 이상 버전** (asyncio 지원을 위해 필요)

### 실행 방법

1. **클라이언트 실행**
```bash
python client.py
```

클라이언트가 실행되면 자동으로 `server.py` 스크립트를 subprocess로 시작하고 MCP 통신을 수행합니다.

### 실행 결과

프로그램을 실행하면 다음과 같은 출력을 확인할 수 있습니다:

```bash
Available tools: [{'name': 'add', 'description': 'Adds two integer numbers together.', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'integer'}, 'b': {'type': 'integer'}}, 'required': ['a', 'b']}}]

Result: {'content': [{'type': 'text', 'text': '8'}], 'isError': False}
```

실행 결과 분석:

**1. Available tools**: 서버에서 제공하는 도구 목록이 표시됩니다
   - `name`: 도구 이름 ("add")
   - `description`: 도구 설명 (함수의 docstring에서 가져옴)
   - `inputSchema`: 입력 파라미터 스키마 (타입 힌팅에서 자동 생성)

**2. Result**: 도구 호출 결과가 MCP 표준 형식으로 반환됩니다
   - `content`: 실제 결과값 (5 + 3 = 8)
   - `isError`: 오류 발생 여부 (false는 성공을 의미)
   - `type`: 반환값 타입 ("text")

## 📚 정리

이 예제는 Model Context Protocol(MCP)의 가장 기본적인 로컬 구현을 보여줍니다. FastMCP 라이브러리를 활용하여 단 몇 줄의 코드로 MCP 서버를 구성하고, `@mcp.tool` 데코레이터로 Python 함수를 MCP 도구로 변환하는 과정을 학습했습니다. 클라이언트에서는 `async/await` 패턴을 사용해 서버에 stdio를 통해 연결하고, `list_tools()`로 사용 가능한 도구를 조회한 후 `call_tool()`로 원격 함수를 실행하는 방법을 다루었습니다. 이 기본 구조는 더 복잡한 MCP 애플리케이션을 구축할 때의 핵심 패턴이 되며, 타입 안정성과 비동기 처리를 통해 안정적인 프로세스 간 통신을 구현하는 MCP의 장점을 잘 보여주는 실용적인 예제입니다.