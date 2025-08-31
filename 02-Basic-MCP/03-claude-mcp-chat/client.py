from fastmcp import Client
from openai import AsyncOpenAI

async def send_llm_request_and_display(llm_client, conversation_history, openai_tools):
    """OpenAI API에 요청을 보내고 응답을 화면에 출력"""
    response = await llm_client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1000,
        messages=conversation_history,
        tools=openai_tools,
    )
    
    # 대화 기록에 응답 저장
    conversation_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content,
        "tool_calls": response.choices[0].message.tool_calls
    })
    
    # 텍스트 응답 출력
    if response.choices[0].message.content:
        print("[🤖 Assistant:]", response.choices[0].message.content)
    
    return response


async def send_tool_request_and_display(response, mcp_client, conversation_history):
    """도구 호출을 실행하고 결과를 대화 기록에 추가"""
    tool_calls = response.choices[0].message.tool_calls
    
    if tool_calls:
        for tool_call in tool_calls:
            print(f"[🔧 Tool Request] {tool_call.function.name}({tool_call.function.arguments})")
            
            # MCP 서버에서 도구 실행
            import json
            args = json.loads(tool_call.function.arguments)
            tool_result = await mcp_client.call_tool(
                tool_call.function.name,
                args
            )
            
            print(f"[✅ Tool Result] {tool_result}")
            
            # OpenAI API 형식으로 변환
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result)
            })

async def main():
    """사용자와 OpenAI의 대화하는 메인 함수"""
    llm_client = AsyncOpenAI()
    conversation_history = []
    
    # MCP 서버 연결 및 도구 설정
    async with Client("http://127.0.0.1:8000/mcp") as mcp_client:
        available_tools = await mcp_client.list_tools()
        openai_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
            }
        } for tool in available_tools]
        
        # 대화 종료 시 까지 반복
        while True:
            # 사용자 입력
            user_input = input("[👤 User]: ")
            conversation_history.append({"role": "user", "content": user_input})
            
            # 도구 호출이 필요 없을 때까지 반복
            while True:
                response = await send_llm_request_and_display(
                    llm_client, conversation_history, openai_tools
                )
                
                if response.choices[0].message.tool_calls:
                    await send_tool_request_and_display(
                        response, mcp_client, conversation_history
                    )
                else:
                    break

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())