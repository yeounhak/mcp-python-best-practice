<div align="center" style="background:#fffbe6; border-radius:20px; box-shadow:0 4px 16px #eee; padding:40px 20px; margin:40px 0;">
  <span style="font-size:1.5em;">🔧</span>
  <div style="margin:10px 0 10px 0;">
    <span style="font-size:1.3em; font-weight:bold; color:#222;">
      Model Context Protocol(MCP)의 기본 구조를 이해하고 </br>
      FastMCP를 활용한 간단한 로컬 클라이언트-서버 통신 방법을 학습할 수 있습니다.
    </span>
  </div>
</div>

## 📋 개요

이 프로젝트는 Model Context Protocol(MCP)의 가장 기본적인 형태를 보여주는 예제입니다. FastMCP 라이브러리를 사용하여 간단한 계산기 서버를 구현하고, 클라이언트에서 이를 호출하는 방법을 다룹니다.

**주요 기술 스택:**
- **FastMCP**: MCP 프로토콜 구현을 위한 Python 라이브러리
- **Python asyncio**: 비동기 프로그래밍을 위한 표준 라이브러리
- **stdio 통신**: 표준 입출력을 통한 프로세스 간 통신

이 예제를 통해 MCP 서버에서 도구를 정의하고 등록하는 방법, 그리고 클라이언트에서 서버에 연결하여 도구를 호출하는 기본적인 패턴을 학습할 수 있습니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/tree/main/02-Basic-MCP/01-local-client-and-server][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/tree/main/02-Basic-MCP/01-local-client-and-server

## 📁 파일 구성

```
01-local-client-and-server/
├── server.py          # MCP 서버 구현 (계산기 도구)
└── client.py          # MCP 클라이언트 구현 (서버 호출)
```

### 주요 파일 설명

**server.py**
```python
# 01-local-client-and-server/server.py 파일입니다.
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

mcp.run()
```

- `CalculatorServer`라는 이름의 MCP 서버를 생성합니다
- `@mcp.tool` 데코레이터를 사용하여 `add` 함수를 MCP 도구로 등록합니다
- `add` 함수는 두 개의 정수를 받아서 더한 결과를 반환하는 간단한 계산기 기능을 제공합니다
- 함수의 docstring은 도구의 설명으로 사용되어 클라이언트에서 확인할 수 있습니다

**client.py**
```python
# 01-local-client-and-server/client.py 파일입니다.
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

- `Client("server.py")`를 통해 로컬 서버 스크립트에 stdio로 연결합니다
- `async with` 구문을 사용하여 클라이언트 연결을 안전하게 관리합니다
- `list_tools()` 메서드로 서버에서 제공하는 도구 목록을 조회합니다
- `call_tool("add", {"a": 5, "b": 3})` 메서드로 특정 도구를 호출하고 매개변수를 전달합니다
- 결과를 출력하여 MCP 통신이 정상적으로 작동하는지 확인합니다

## 🚀 실행

### 사전 요구사항

**1. Python 패키지 설치**
```bash
pip install fastmcp
```

FastMCP 라이브러리만 있으면 이 예제를 실행할 수 있습니다. 추가적인 외부 API 키나 설정은 필요하지 않습니다.

### 실행 방법

**1. MCP 클라이언트 실행**
```bash
python client.py
```

클라이언트를 실행하면 자동으로 `server.py`를 subprocess로 시작하고 MCP 프로토콜을 통해 통신합니다.

### 실행 결과

실제로 프로그램을 실행하면 다음과 같은 출력을 확인할 수 있습니다:

```bash
Available tools: [{'name': 'add', 'description': 'Adds two integer numbers together.', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'integer'}, 'b': {'type': 'integer'}}, 'required': ['a', 'b']}}]

Result: {'content': [{'type': 'text', 'text': '8'}], 'isError': False}
```

**1. Available tools**: 서버에서 제공하는 도구 목록이 표시됩니다
   - `name`: 도구 이름 ("add")
   - `description`: 도구 설명 ("Adds two integer numbers together.")
   - `inputSchema`: 도구가 받는 매개변수의 JSON 스키마 정보

**2. Result**: 도구 호출 결과가 MCP 표준 형식으로 반환됩니다
   - `content`: 실제 결과값이 텍스트 형태로 포함됩니다 ("8")
   - `isError`: 오류 발생 여부를 나타냅니다 (False = 성공)

이 결과를 통해 클라이언트가 성공적으로 서버에 연결하고, 서버의 `add` 도구를 호출하여 5 + 3 = 8이라는 계산 결과를 받았음을 확인할 수 있습니다.

## 📚 정리

이 예제는 Model Context Protocol(MCP)의 가장 기본적인 형태를 보여줍니다. FastMCP 라이브러리를 활용하여 몇 줄의 코드만으로 MCP 서버를 구성하고, `@mcp.tool` 데코레이터로 함수를 도구로 등록하는 과정을 다루었습니다. 클라이언트에서는 `async/await` 패턴을 사용해 서버에 안전하게 연결하고, `list_tools()`로 사용 가능한 도구를 조회한 후 `call_tool()`로 원격 함수를 실행하는 방법을 학습했습니다. 

특히 주목할 점은 stdio를 통한 프로세스 간 통신 방식으로, 이는 MCP의 핵심 특징 중 하나입니다. 클라이언트와 서버가 별도의 프로세스로 실행되면서도 표준 입출력을 통해 구조화된 JSON-RPC 메시지를 주고받는 방식은 다양한 언어와 환경 간의 상호운용성을 보장합니다. 이러한 기본 패턴을 이해하면 더 복잡한 MCP 애플리케이션을 구축할 때 필요한 토대를 마련할 수 있습니다.