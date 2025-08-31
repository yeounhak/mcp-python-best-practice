<div align="center" style="background:#fffbe6; border-radius:20px; box-shadow:0 4px 16px #eee; padding:40px 20px; margin:40px 0;">
  <span style="font-size:1.5em;">🤖</span>
  <div style="margin:10px 0 10px 0;">
    <span style="font-size:1.3em; font-weight:bold; color:#222;">
      OpenAI GPT-4와 MCP 서버를 연결하여 도구 기능을 활용하는 </br>
      대화형 AI 시스템 구현 방법을 학습할 수 있습니다.
    </span>
  </div>
</div>

## 📋 개요

이 프로젝트는 Model Context Protocol(MCP) 서버와 OpenAI GPT-4 API를 통합하여 대화형 AI 시스템을 구현한 예제입니다. 클라이언트는 사용자의 자연어 입력을 받아 GPT-4가 해석하게 하고, 필요시 MCP 서버의 도구를 자동으로 호출하여 결과를 다시 GPT-4에 전달하는 완전한 AI 워크플로우를 보여줍니다.

주요 기술 스택은 다음과 같습니다:
- **FastMCP**: MCP 클라이언트 및 서버 구현을 위한 Python 라이브러리
- **OpenAI Python SDK**: GPT-4 API와의 비동기 통신을 위한 공식 SDK  
- **asyncio**: 비동기 프로그래밍을 통한 효율적인 API 호출 관리

이 구현은 LLM이 외부 도구를 활용하여 복잡한 작업을 수행할 수 있는 Agent 패턴의 기본 구조를 제공하며, MCP 표준을 따라 도구 호출과 결과 처리를 안전하게 관리합니다.

> 🔗 **상세 코드 및 예제**: [https://github.com/yeounhak/mcp-python-best-practice/02/Basic-MCP/03-claude-mcp-chat][github-repo]

[github-repo]: https://github.com/yeounhak/mcp-python-best-practice/02/Basic-MCP/03-claude-mcp-chat

## 📁 파일 구성

```
03-claude-mcp-chat/
├── client.py          # OpenAI GPT-4와 MCP 서버를 연결하는 클라이언트
└── server.py          # 계산기 도구를 제공하는 MCP 서버
```

### 주요 파일 설명

**server.py**
```python
# 03-claude-mcp-chat/server.py 파일입니다.
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

mcp.run(transport='http')
```

- HTTP 전송 방식을 사용하는 간단한 MCP 서버 구현
- `add` 함수를 MCP 도구로 등록하여 두 정수의 덧셈 기능 제공
- 포트 8000에서 HTTP 서버로 실행되어 클라이언트의 연결을 대기

**client.py**
```python
# 03-claude-mcp-chat/client.py 파일입니다.
import json
import asyncio
from fastmcp import Client
from openai import AsyncOpenAI


async def ask_llm_and_get_response(llm_client, messages, available_tools):
    """LLM에게 질문하고 답변을 받기"""
    
    # LLM에게 질문 보내기
    response = await llm_client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1000,
        messages=messages,
        tools=available_tools
    )
    
    # LLM의 답변을 대화 기록에 저장
    llm_message = {
        "role": "assistant",
        "content": response.choices[0].message.content,
        "tool_calls": response.choices[0].message.tool_calls
    }
    messages.append(llm_message)
    
    # LLM이 텍스트로 답변했다면 화면에 출력
    if response.choices[0].message.content:
        print("[🤖 LLM 답변] ", response.choices[0].message.content)
    
    return response


async def run_tools_and_get_results(llm_response, mcp_server, messages):
    """LLM이 요청한 도구들을 실행하고 결과 얻기"""
    
    # LLM이 도구 사용을 요청했는지 확인
    tool_calls = llm_response.choices[0].message.tool_calls
    if not tool_calls:
        return
    
    # 요청된 각 도구를 실행
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_arguments = tool_call.function.arguments
        
        print(f"[🔧 도구 실행] {tool_name}({tool_arguments})")
        
        # 도구 실행하기
        arguments = json.loads(tool_arguments)
        result = await mcp_server.call_tool(tool_name, arguments)
        
        print(f"[✅ 실행 결과] {result}")
        
        # 도구 실행 결과를 대화 기록에 저장
        tool_result_message = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        }
        messages.append(tool_result_message)


def convert_mcp_tools_to_openai_format(mcp_tools):
    """MCP 도구들을 OpenAI 형식으로 변환"""
    
    openai_tools = []
    
    for tool in mcp_tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
            }
        }
        openai_tools.append(openai_tool)
    
    return openai_tools


def check_if_llm_wants_to_use_tools(llm_response):
    """LLM이 도구를 사용하고 싶어하는지 확인"""
    return llm_response.choices[0].message.tool_calls is not None


async def main():
    """사용자와 LLM이 대화하는 메인 프로그램"""
    
    # OpenLLM 클라이언트 준비
    llm_client = AsyncOpenAI()
    
    # 대화 기록을 저장할 리스트
    conversation_history = []
    
    # MCP 서버에 연결
    async with Client("http://127.0.0.1:8000/mcp") as mcp_server:
        
        # 사용 가능한 도구들 가져오기
        mcp_tools = await mcp_server.list_tools()
        
        # MCP 도구들을 OpenAI 형식으로 변환
        openai_tools = convert_mcp_tools_to_openai_format(mcp_tools)
        
        # 사용자와 계속 대화하기
        while True:
            # 사용자 입력 받기
            user_message = input("[👤 사용자] ")
            
            # 사용자 메시지를 대화 기록에 추가
            conversation_history.append({
                "role": "user", 
                "content": user_message
            })
            
            # LLM이 도구를 사용하지 않을 때까지 반복
            while True:
                # LLM에게 질문하고 답변 받기
                llm_response = await ask_llm_and_get_response(
                    llm_client, 
                    conversation_history, 
                    openai_tools
                )
                
                # LLM이 도구를 사용하고 싶어한다면
                if check_if_llm_wants_to_use_tools(llm_response):
                    # 도구들을 실행하고 결과 얻기
                    await run_tools_and_get_results(
                        llm_response, 
                        mcp_server, 
                        conversation_history
                    )
                else:
                    # LLM이 더 이상 도구를 사용하지 않으니 대화 턴 종료
                    break


if __name__ == '__main__':
    asyncio.run(main())
```

- `ask_llm_and_get_response()`: OpenAI GPT-4 API에 메시지를 전송하고 응답을 받는 핵심 함수
- `run_tools_and_get_results()`: LLM이 요청한 도구들을 MCP 서버에서 실행하고 결과를 수집
- `convert_mcp_tools_to_openai_format()`: MCP 도구 스키마를 OpenAI Function Calling 형식으로 변환
- `check_if_llm_wants_to_use_tools()`: LLM 응답에 도구 호출 요청이 포함되었는지 확인
- 대화 기록(`conversation_history`)을 통해 컨텍스트를 유지하며 연속적인 대화 지원
- 비동기 컨텍스트 매니저를 사용하여 MCP 서버와의 안전한 연결 관리

## 🚀 실행

### 사전 요구사항

**1. Python 패키지 설치**
```bash
pip install fastmcp openai
```

**2. OpenAI API 키 설정**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 실행 방법

**1. MCP 서버 실행 (터미널 1)**
```bash
python server.py
```

**2. 클라이언트 실행 (터미널 2)**
```bash
python client.py
```

### 실행 결과

실제로 프로그램을 실행하면 다음과 같은 대화형 인터페이스가 시작됩니다:

```bash
[👤 사용자] 15와 27을 더해줘
[🤖 LLM 답변] 15와 27을 더해보겠습니다.
[🔧 도구 실행] add({"a": 15, "b": 27})
[✅ 실행 결과] {'content': [{'type': 'text', 'text': '42'}], 'isError': False}
[🤖 LLM 답변] 15와 27을 더한 결과는 42입니다.

[👤 사용자] 100과 200을 더한 다음 50을 더해줘
[🤖 LLM 답변] 먼저 100과 200을 더해보겠습니다.
[🔧 도구 실행] add({"a": 100, "b": 200})
[✅ 실행 결과] {'content': [{'type': 'text', 'text': '300'}], 'isError': False}
[🤖 LLM 답변] 이제 300에 50을 더해보겠습니다.
[🔧 도구 실행] add({"a": 300, "b": 50})
[✅ 실행 결과] {'content': [{'type': 'text', 'text': '350'}], 'isError': False}
[🤖 LLM 답변] 100과 200을 더한 결과는 300이고, 여기에 50을 더한 최종 결과는 350입니다.
```

위 예시에서 확인할 수 있는 주요 동작 과정:

**1. 사용자 입력 처리**: 자연어로 입력된 계산 요청을 GPT-4가 이해하고 적절한 도구 호출로 변환

**2. 도구 호출 및 실행**: LLM이 `add` 도구를 올바른 매개변수와 함께 호출하여 MCP 서버에서 실행

**3. 결과 통합**: 도구 실행 결과를 다시 LLM에게 전달하여 사용자에게 친화적인 형태로 응답 생성

**4. 연속 대화**: 복잡한 계산의 경우 여러 번의 도구 호출을 통해 단계별로 문제를 해결

**5. 컨텍스트 유지**: 대화 기록을 통해 이전 계산 결과를 활용한 연속적인 작업 수행

## 📚 정리

이 예제는 OpenAI GPT-4와 Model Context Protocol을 결합한 실용적인 AI Agent 시스템의 구현을 보여줍니다. 핵심적으로는 LLM의 자연어 이해 능력과 MCP 서버의 구체적인 도구 실행 능력을 연결하여, 사용자가 복잡한 API 호출이나 프로그래밍 없이도 자연어만으로 도구를 활용할 수 있게 합니다. 클라이언트 코드에서 가장 중요한 부분은 OpenAI Function Calling 형식과 MCP 도구 스키마 간의 변환 로직과, 대화 컨텍스트를 유지하면서 도구 호출 결과를 LLM에게 다시 전달하는 순환 구조입니다. 이러한 패턴은 단순한 계산기를 넘어서 파일 처리, 데이터베이스 조작, 웹 API 호출 등 다양한 도구로 확장 가능하며, 실제 프로덕션 환경에서 AI Agent를 구현할 때의 기본 아키텍처를 제공합니다. 특히 비동기 프로그래밍과 에러 처리, 도구 결과의 구조화된 관리 방식은 안정적인 AI 시스템 개발에 필수적인 요소들을 잘 보여주고 있습니다.