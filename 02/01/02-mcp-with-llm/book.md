## 📋 개요

이 프로젝트는 MCP(Model Context Protocol)와 Claude LLM을 통합하여 대화형 도구 호출 시스템을 구현한 예제입니다. FastMCP 프레임워크를 사용하여 MCP 서버를 구축하고, Anthropic의 Claude API를 통해 자연어로 도구를 호출할 수 있는 완전한 워크플로우를 보여줍니다.

주요 특징:
- **MCP 서버**: FastMCP를 사용한 간단한 계산기 도구 서버
- **Claude LLM 통합**: Anthropic Claude API를 통한 자연어 처리
- **대화형 인터페이스**: 사용자와 AI 간의 실시간 대화 시스템
- **도구 호출 자동화**: LLM이 필요에 따라 자동으로 MCP 도구 호출

이 예제는 MCP의 핵심 개념과 LLM과의 통합 방법을 학습하기에 적합하며, 더 복잡한 도구 시스템을 구축하기 위한 기초를 제공합니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02/01/02-mcp-with-llm][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02/01/02-mcp-with-llm

## 📁 파일 구성

```
02-mcp-with-llm/
├── server.py          # MCP 서버 구현 (계산기 도구)
└── client.py          # Claude LLM과 통합된 클라이언트
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
- FastMCP를 사용하여 `CalculatorServer` 이름의 MCP 서버 생성
- `@mcp.tool` 데코레이터로 `add` 함수를 MCP 도구로 등록
- 두 정수 매개변수를 받아 합계를 반환하는 간단한 계산기 기능
- `mcp.run()`으로 서버를 시작하여 클라이언트 연결 대기

**client.py**
```python
from fastmcp import Client
from anthropic import AsyncAnthropic

async def main():
    llm_client = AsyncAnthropic()
    conversation_history = []
    
    async with Client("server.py") as mcp_client:
        available_tools = await mcp_client.list_tools()
        anthropic_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
        } for tool in available_tools]
        
        while True:
            user_input = input("[👤 User]: ")
            conversation_history.append({"role": "user", "content": user_input})
            
            response = await llm_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=conversation_history,
                tools=anthropic_tools,
            )
            
            if response.stop_reason == "tool_use":
                # 도구 호출 실행 및 결과 처리
                tool_result = await mcp_client.call_tool(...)
```
- Anthropic Claude API와 FastMCP Client를 통합하여 대화형 시스템 구현
- `mcp_client.list_tools()`로 사용 가능한 MCP 도구 조회 후 Anthropic API 형식으로 변환
- 사용자 입력을 `conversation_history`에 저장하여 대화 컨텍스트 유지
- Claude가 도구 호출이 필요하다고 판단하면 자동으로 MCP 서버의 함수 실행
- `async/await` 패턴으로 비동기 API 호출과 실시간 사용자 인터랙션 처리

## 🚀 실행

### 사전 요구사항

1. **Python 패키지 설치**
```bash
pip install fastmcp anthropic
```

2. **Anthropic API 키 설정**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 실행 방법

1. **MCP 서버 및 클라이언트 실행**
```bash
python client.py
```

### 실행 결과

실제로 프로그램을 실행하면 다음과 같은 대화형 인터페이스가 시작됩니다:

```bash
[👤 User]: 15와 27을 더해줘

[🤖 Assistant:] 15와 27을 더해보겠습니다.

[🔧 Tool Request] add({'a': 15, 'b': 27})

[✅ Tool Result] 42

[🤖 Assistant:] 15와 27을 더한 결과는 42입니다.
```

위 예시에서 확인할 수 있듯이:
- 사용자가 자연어로 수학 계산을 요청하면
- Claude가 요청을 이해하고 적절한 MCP 도구(`add`)를 선택
- MCP 서버에서 실제 계산을 수행하고 결과를 반환
- 최종적으로 자연어로 결과를 사용자에게 제공

이러한 흐름을 통해 복잡한 프로토콜 호출이 사용자에게는 자연스러운 대화로 추상화됩니다.


## 📚 정리

이 예제는 MCP(Model Context Protocol)와 Claude LLM을 통합한 대화형 도구 호출 시스템의 구현 방법을 보여줍니다. FastMCP 프레임워크를 활용하여 간단한 계산기 도구 서버를 구축하고, Anthropic Claude API를 통해 자연어로 도구를 호출할 수 있는 완전한 워크플로우를 구현했습니다. 

특히 주목할 점은 사용자가 자연어로 "15와 27을 더해줘"라고 입력하면, Claude가 자동으로 적절한 MCP 도구를 선택하여 `add({'a': 15, 'b': 27})`를 호출하고, 결과를 대화 컨텍스트에 통합하여 자연스러운 응답을 제공한다는 것입니다. 이는 복잡한 계산도 단계별로 분해하여 처리할 수 있으며, `async/await` 패턴을 통한 비동기 프로그래밍으로 효율적인 API 호출과 논블로킹 사용자 인터페이스를 구현했습니다. 

이 통합 패턴은 계산기 봇, 데이터 분석 도구, 시스템 관리, 정보 검색 등 다양한 실제 활용 시나리오에 적용할 수 있으며, 더 많은 도구 추가, 복합 연산 처리, 상태 관리, 외부 API 통합 등으로 확장 가능합니다. 결과적으로 MCP와 LLM을 결합한 실용적인 AI 도구 시스템 구축의 기초를 제공하며, 향후 더 정교하고 복잡한 시스템 개발을 위한 견고한 출발점으로 활용할 수 있습니다.