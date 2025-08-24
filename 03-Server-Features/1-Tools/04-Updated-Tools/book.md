## 📋 개요

이 프로젝트는 Model Context Protocol(MCP)에서 동적 도구 활성화 기능을 보여주는 예제입니다. FastMCP 프레임워크를 사용하여 MCP 서버와 클라이언트를 구현하며, 특히 `hello_tool` 실행 시 비활성화된 `add_tool`을 동적으로 활성화하는 기능을 다룹니다. 

주요 기술 스택:
- **FastMCP**: Python용 MCP 구현 프레임워크
- **asyncio**: 비동기 프로그래밍 지원
- **HTTP 전송**: 클라이언트-서버 통신 방식

이 예제를 통해 MCP에서 도구의 상태를 런타임에 동적으로 변경하고, 클라이언트가 이러한 변경사항을 감지하여 처리하는 방법을 학습할 수 있습니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/1-Tools/04-Updated-Tools][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/03-Server-Features/1-Tools/04-Updated-Tools

## 📁 파일 구성

```
04-Updated-Tools/
├── server.py          # MCP 서버 구현 (동적 도구 활성화)
└── client.py          # MCP 클라이언트 구현 (메시지 핸들러 포함)
```

### 주요 파일 설명

**server.py**

**1. FastMCP 서버 초기화 및 hello_tool 구현**
```python
from fastmcp import FastMCP

# FastMCP 인스턴스 생성
mcp = FastMCP()

@mcp.tool
def hello_tool() -> str:
    add_tool.enable()
    return "Hello!"
```
- FastMCP 인스턴스를 생성하여 MCP 서버 구성
- `hello_tool`은 기본적으로 활성화된 도구로, 실행 시 `add_tool.enable()` 호출
- "Hello!" 문자열을 반환하는 간단한 기능

**2. 동적으로 활성화되는 add_tool 구현**
```python
@mcp.tool(enabled=False)
def add_tool(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b
```
- `enabled=False` 파라미터로 초기에는 비활성화 상태로 설정
- 두 정수를 받아 더한 결과를 반환하는 계산기 기능
- `hello_tool` 실행 후에만 사용 가능해짐

**3. HTTP 서버 실행 설정**
```python
mcp.run(
    transport="http",
    host="0.0.0.0",
    port=9000,
)
```
- HTTP 프로토콜을 사용하여 포트 9000에서 서버 실행
- 모든 인터페이스에서 접근 가능하도록 0.0.0.0 호스트 설정

**client.py**

**1. 메시지 핸들러 구현**
```python
from fastmcp import Client

async def message_handler(message):
    """서버로부터 오는 모든 MCP 메시지를 처리합니다."""
    if hasattr(message, 'root'):
        method = message.root.method
        print(f"📨 수신됨: {method}")
        
        # 특정 알림 처리
        if method == "notifications/tools/list_changed":
            print("🔄 도구가 변경되어 list_tools를 다시 호출하세요")
```
- 서버로부터 오는 모든 MCP 메시지를 처리하는 핸들러 함수
- `notifications/tools/list_changed` 알림을 감지하여 도구 변경 상황 처리
- 메시지 타입별로 적절한 응답 제공

**2. 클라이언트 연결 및 도구 호출**
```python
async def main():
    async with Client(
            "http://0.0.0.0:9000/mcp",
            message_handler=message_handler,
        ) as client:
        tools = await client.list_tools()
        print(f"\n🛠️ 사용 가능한 도구: {[tool.name for tool in tools]}")
        
        result = await client.call_tool("hello_tool")
        print(f"\n✅ 결과: {result}")
```
- HTTP를 통해 MCP 서버에 연결
- 메시지 핸들러를 등록하여 서버 알림 수신
- `list_tools()`로 사용 가능한 도구 목록 조회
- `hello_tool` 호출 및 결과 출력

**3. 도구 상태 변경 확인 및 추가 도구 호출**
```python
        # hello_tool 호출 후 도구가 변경되었는지 확인
        tools_after = await client.list_tools()
        print(f"\n🔍 hello_tool 실행 후 사용 가능한 도구: {[tool.name for tool in tools_after]}")
        
        result = await client.call_tool("add_tool", {"a": 5, "b": 3})
        print(f"\n✅ 결과: {result}")
```
- `hello_tool` 실행 후 도구 목록을 다시 조회하여 변경사항 확인
- 새롭게 활성화된 `add_tool`을 호출하여 덧셈 연산 수행
- 매개변수로 딕셔너리 형태의 데이터 전달

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp
```

2. **Python 3.7 이상 환경**
- asyncio 지원을 위해 Python 3.7 이상 버전 필요

### 실행 방법

1. **MCP 서버 시작**
```bash
python server.py
```

2. **별도 터미널에서 클라이언트 실행**
```bash
python client.py
```

### 실행 결과

실제로 프로그램을 실행하면 다음과 같은 출력을 확인할 수 있습니다:

```bash
🛠️ 사용 가능한 도구: ['hello_tool']

✅ 결과: Hello!
📨 수신됨: notifications/tools/list_changed
🔄 도구가 변경되어 list_tools를 다시 호출하세요

🔍 hello_tool 실행 후 사용 가능한 도구: ['hello_tool', 'add_tool']

✅ 결과: 8
```

위 실행 결과에서 확인할 수 있는 주요 흐름:

1. **초기 상태**: `hello_tool`만 사용 가능한 상태로 시작
2. **hello_tool 실행**: "Hello!" 메시지 반환과 동시에 `add_tool` 활성화
3. **알림 수신**: 서버에서 `notifications/tools/list_changed` 알림 전송
4. **도구 목록 변경 확인**: `add_tool`이 새롭게 추가된 것을 확인
5. **add_tool 실행**: 5 + 3 = 8 연산 결과 반환

## 📚 정리

이 예제는 Model Context Protocol에서 도구의 동적 활성화 기능을 구현하는 방법을 보여줍니다. FastMCP 프레임워크의 `enabled=False` 파라미터를 통해 초기에 비활성화된 도구를 생성하고, 다른 도구의 실행 결과로 `.enable()` 메서드를 호출하여 런타임에 도구를 활성화하는 과정을 다루었습니다. 클라이언트 측에서는 메시지 핸들러를 구현하여 `notifications/tools/list_changed` 알림을 수신하고, 도구 목록의 변경사항을 실시간으로 감지하는 방법을 학습했습니다. 이러한 동적 도구 관리 기능은 조건부 기능 제공, 단계별 워크플로우 구현, 권한 기반 도구 접근 등 다양한 시나리오에서 활용할 수 있으며, MCP의 유연성과 확장성을 보여주는 중요한 기능입니다.