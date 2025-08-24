## 개요

이 예제는 Model Context Protocol(MCP)를 사용하여 클라이언트와 서버 간의 기본적인 통신을 구현합니다. LLM(대규모 언어 모델) 없이 직접적으로 도구를 호출하고 결과를 받아오는 방법을 보여줍니다.
자세한 내용은 https://github.com/yeounhak/mcp-python-best-practice/02/01/01-mcp-without-llm 를 확인해주세요.

## 1. MCP 서버 (server.py)

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

## 2. MCP 클라이언트 (client.py)

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

## 실행 방법

1. **클라이언트 실행**: `python client.py` 명령어 실행

## 실행 결과

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

## 핵심 개념

- **MCP**: Model Context Protocol의 약자로, 클라이언트와 서버 간의 표준화된 통신 프로토콜
- **stdio 통신**: 표준 입출력을 통한 프로세스 간 통신 방식
- **비동기 처리**: `async/await`를 사용한 비동기 프로그래밍 패턴