## 📋 개요

이 예제는 Model Context Protocol(MCP)를 사용하여 클라이언트와 서버 간의 기본적인 통신을 구현합니다. LLM(대규모 언어 모델) 없이 직접적으로 도구를 호출하고 결과를 받아오는 방법을 보여줍니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02/01/01-mcp-without-llm][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02/01/01-mcp-without-llm

## 📁 파일 구성

### 1. MCP 서버 (server.py)

```python
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

mcp.run()
```

**주요 특징:**
- `FastMCP`를 사용하여 MCP 서버를 간단하게 구성
- `@mcp.tool` 데코레이터를 사용하여 함수를 MCP 도구로 등록
- `add` 함수는 두 정수를 더하는 기본적인 계산 기능 제공
- 함수에 docstring을 포함하여 도구의 설명 제공

### 2. MCP 클라이언트 (client.py)

```python
from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"Result: {result.text}")
        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

**주요 특징:**
- `Client` 클래스를 사용하여 서버에 연결
- `async with` 구문으로 안전한 연결 관리
- `list_tools()`로 사용 가능한 도구 목록 조회
- `call_tool()`로 특정 도구 실행 및 결과 받기

## 🚀 실행 

**클라이언트 실행**: `python client.py` 명령어 실행
클라이언트를 실행하면 다음과 같은 결과를 확인할 수 있습니다:

### 1. 사용 가능한 도구 목록 출력
```
Available tools: [Tool(name='add', title=None, description='Adds two integer numbers together.', inputSchema={'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'type': 'object'}, outputSchema={'properties': {'result': {'title': 'Result', 'type': 'integer'}}, 'required': ['result'], 'title': '_WrappedResult', 'type': 'object', 'x-fastmcp-wrap-result': True}, annotations=None, meta={'_fastmcp': {'tags': []}})]
```

**분석:**
- `name`: 도구 이름 (`add`)
- `description`: 도구 설명 
- `inputSchema`: 입력 매개변수 스키마 (정수형 a, b 필요)
- `outputSchema`: 출력 스키마 (정수형 result 반환)

### 2. 도구 실행 결과 출력
```
Result: CallToolResult(content=[TextContent(type='text', text='8', annotations=None, meta=None)], structured_content={'result': 8}, data=8, is_error=False)
```

**분석:**
- `content`: 텍스트 형태의 결과 ('8')
- `structured_content`: 구조화된 데이터 (`{'result': 8}`)
- `data`: 실제 반환값 (8)
- `is_error`: 오류 발생 여부 (False)

## 📚 정리

이 예제는 Model Context Protocol(MCP)의 가장 기본적인 형태를 보여줍니다. FastMCP 라이브러리를 활용하여 몇 줄의 코드만으로 MCP 서버를 구성하고, `@mcp.tool` 데코레이터로 함수를 도구로 등록하는 과정을 다루었습니다. 클라이언트에서는 `async/await` 패턴을 사용해 서버에 안전하게 연결하고, `list_tools()`로 사용 가능한 도구를 조회한 후 `call_tool()`로 원격 함수를 실행하는 방법을 학습했습니다. 

특히 이 예제는 LLM 없이도 직접적인 도구 호출이 가능함을 보여주며, 입력/출력 스키마를 통한 타입 안전성과 구조화된 데이터 처리 방식을 경험할 수 있습니다. 실행 결과를 통해 MCP의 도구 메타데이터 구조와 `CallToolResult` 객체의 다양한 속성들을 이해할 수 있어, 향후 더 복잡한 MCP 애플리케이션 개발의 기초가 됩니다.

