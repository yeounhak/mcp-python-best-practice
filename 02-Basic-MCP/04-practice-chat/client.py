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