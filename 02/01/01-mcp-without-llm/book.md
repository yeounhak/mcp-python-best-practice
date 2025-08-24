# MCP 기본 예제 - LLM 없이 직접 통신

## 개요

이 예제는 Model Context Protocol(MCP)를 사용하여 클라이언트와 서버 간의 기본적인 통신을 구현합니다. LLM(대규모 언어 모델) 없이 직접적으로 도구를 호출하고 결과를 받아오는 방법을 보여줍니다.
자세한 내용은 https://github.com/yeounhak/mcp-python-best-practice.git

## 구성 요소

### 1. 서버 (server.py)

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

### 2. 클라이언트 (client.py)

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

1. **서버 실행**: 별도 터미널에서 `python server.py` 실행
2. **클라이언트 실행**: 다른 터미널에서 `python client.py` 실행

## 통신 과정

1. 클라이언트가 서버에 연결을 시도합니다
2. 서버로부터 사용 가능한 도구 목록을 받아옵니다
3. 특정 도구(`add`)를 매개변수와 함께 호출합니다
4. 서버가 계산을 수행하고 결과를 반환합니다
5. 클라이언트가 결과를 출력합니다

## 학습 포인트

- **MCP의 기본 구조**: 서버와 클라이언트의 역할 분리
- **도구 등록**: `@mcp.tool` 데코레이터 사용법
- **비동기 통신**: `async/await` 패턴의 활용
- **stdio 통신**: 표준 입출력을 통한 프로세스 간 통신
- **타입 힌팅**: Python의 타입 힌트를 활용한 명확한 인터페이스 정의

## 확장 가능성

이 기본 예제를 바탕으로 다음과 같은 기능을 추가할 수 있습니다:
- 더 복잡한 계산 도구들
- 파일 시스템 접근 도구
- 데이터베이스 연동 도구
- 웹 API 호출 도구
- 에러 처리 및 검증 로직

## 다음 단계

이 예제를 이해했다면 다음 단계로 넘어갈 수 있습니다:
1. LLM과 연동하는 MCP 예제
2. 복수의 도구를 가진 서버 구현
3. 리소스(파일, URL 등) 처리하는 MCP 서버
4. 실제 프로덕션 환경에서의 MCP 활용