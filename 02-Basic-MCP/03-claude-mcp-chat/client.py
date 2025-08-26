from fastmcp import Client
from anthropic import AsyncAnthropic

async def send_llm_request_and_display(llm_client, conversation_history, anthropic_tools):
    """Claude API에 요청을 보내고 응답을 화면에 출력"""
    response = await llm_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=conversation_history,
        tools=anthropic_tools,
    )
    
    # 대화 기록에 응답 저장
    conversation_history.append({
        "role": "assistant",
        "content": response.content
    })
    
    # 텍스트 응답 출력
    for content_block in response.content:
        if content_block.type == "text":
            print("[🤖 Assistant:]", content_block.text)
    
    return response


async def send_tool_request_and_display(response, mcp_client, conversation_history):
    """도구 호출을 실행하고 결과를 대화 기록에 추가"""
    tool_results = []
    
    for content_block in response.content:
        if content_block.type == "tool_use":
            print(f"[🔧 Tool Request] {content_block.name}({content_block.input})")
            
            # MCP 서버에서 도구 실행
            tool_result = await mcp_client.call_tool(
                content_block.name,
                content_block.input
            )
            
            print(f"[✅ Tool Result] {tool_result}")
            
            # Anthropic API 형식으로 변환
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": content_block.id,
                "content": str(tool_result)
            })
    
    # 도구 결과를 대화 기록에 추가
    conversation_history.append({"role": "user", "content": tool_results})

async def main():
    """사용자와 Claude의 대화하는 메인 함수"""
    llm_client = AsyncAnthropic()
    conversation_history = []
    
    # MCP 서버 연결 및 도구 설정
    async with Client("server.py") as mcp_client:
        available_tools = await mcp_client.list_tools()
        anthropic_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
        } for tool in available_tools]
        
        # 대화 종료 시 까지 반복
        while True:
            # 사용자 입력
            user_input = input("[👤 User]: ")
            conversation_history.append({"role": "user", "content": user_input})
            
            # 도구 호출이 필요 없을 때까지 반복
            while True:
                response = await send_llm_request_and_display(
                    llm_client, conversation_history, anthropic_tools
                )
                
                if response.stop_reason == "tool_use":
                    await send_tool_request_and_display(
                        response, mcp_client, conversation_history
                    )
                else:
                    break

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())