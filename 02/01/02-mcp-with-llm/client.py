from fastmcp import Client  # MCP(Model Context Protocol) 클라이언트
from anthropic import AsyncAnthropic  # Anthropic Claude API 클라이언트

async def send_llm_request_and_display(llm_client, conversation_history, anthropic_tools):
    """Claude API에 메시지를 전송하고 응답을 화면에 출력하는 함수"""
    
    # Claude API에 요청 보내기
    # - model: 사용할 Claude 모델 버전
    # - max_tokens: 최대 응답 토큰 수 제한
    # - messages: 지금까지의 대화 내역
    # - tools: 사용 가능한 도구 목록 (계산기 등)
    response = await llm_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=conversation_history,
        tools=anthropic_tools,
    )
    
    # Claude의 응답을 대화 기록에 저장
    # 이렇게 해야 다음 대화에서 이전 맥락을 기억할 수 있음
    conversation_history.append({
        "role": "assistant",  # 어시스턴트가 보낸 메시지임을 표시
        "content": response.content  # 실제 응답 내용
    })
    
    # Claude의 텍스트 응답만 골라서 화면에 출력
    # (도구 호출 요청은 여기서 출력하지 않고, 별도로 처리)
    for content_block in response.content:
        if content_block.type == "text":
            print("[🤖 Assistant:]", content_block.text)
    
    # 응답 객체를 반환 (도구 호출이 필요한지 확인하기 위해)
    return response


async def send_tool_request_and_display(response, mcp_client, conversation_history):
    """Claude가 요청한 도구(계산기 등)를 실행하고 결과를 화면에 표시"""
    
    tool_results = []  # 모든 도구 실행 결과를 모을 리스트
    
    # Claude 응답에서 도구 호출 요청들을 찾아서 처리
    for content_block in response.content:
        if content_block.type == "tool_use":  # 도구 사용 요청인 경우
            
            # 사용자에게 어떤 도구를 호출하는지 보여주기
            # 예: [🔧 Tool Request] add({'a': 999, 'b': 888})
            print(f"[🔧 Tool Request] {content_block.name}({content_block.input})")
            
            # 실제로 MCP 서버(server.py)에 도구 실행 요청
            # 예: add 함수에 999와 888을 전달해서 계산 실행
            tool_result = await mcp_client.call_tool(
                content_block.name,  # 도구 이름 (예: "add")
                content_block.input  # 도구에 전달할 입력값 (예: {'a': 999, 'b': 888})
            )
            
            # 도구 실행 결과를 사용자에게 보여주기
            # 예: [✅ Tool Result] CallToolResult(content=[...], data=1887, ...)
            print(f"[✅ Tool Result] {tool_result}")
            print()  # 가독성을 위한 빈 줄 추가
            
            # Claude가 이해할 수 있는 형식으로 결과 변환
            # Anthropic API가 요구하는 특정 형식에 맞춰야 함
            tool_results.append({
                "type": "tool_result",  # 이것이 도구 실행 결과임을 표시
                "tool_use_id": content_block.id,  # 어떤 도구 요청에 대한 결과인지 식별
                "content": str(tool_result)  # 실제 결과 내용
            })
    
    # 모든 도구 실행 결과를 대화 기록에 추가
    # Claude는 이 결과를 보고 최종 답변을 생성함
    conversation_history.append({
        "role": "user",  # 도구 결과는 사용자 메시지로 취급
        "content": tool_results  # 모든 도구 실행 결과들
    })

async def main():
    """메인 함수: 사용자와 Claude의 대화를 중계하는 채팅 프로그램"""
    
    # Anthropic Claude API 클라이언트 초기화
    # 환경변수 ANTHROPIC_API_KEY에서 API 키를 자동으로 읽어옴
    llm_client = AsyncAnthropic()
    
    # 대화 내역을 저장할 리스트
    # Claude가 이전 대화를 기억할 수 있도록 모든 메시지를 누적 저장
    conversation_history = []
    
    # MCP 서버(server.py)와 연결
    # 이 서버에는 계산기 등의 도구들이 구현되어 있음
    async with Client("server.py") as mcp_client:
        
        # MCP 서버에서 사용 가능한 도구 목록 가져오기
        # 예: add(덧셈) 함수 등
        available_tools = await mcp_client.list_tools()
        
        # MCP 형식의 도구 정보를 Anthropic API 형식으로 변환
        # Claude가 이해할 수 있는 형태로 바꿔야 함
        anthropic_tools = [{
            "name": tool.name,  # 도구 이름 (예: "add")
            "description": tool.description,  # 도구 설명 (예: "두 정수를 더합니다")
            "input_schema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}  # 입력 형식
        } for tool in available_tools]
        
        # 무한 대화 루프 시작
        while True:
            # 사용자로부터 입력 받기
            print()  # 가독성을 위한 빈 줄
            user_input = input("[👤 User]: ")
            
            # 사용자 입력을 대화 기록에 추가
            conversation_history.append({
                "role": "user",  # 사용자가 보낸 메시지임을 표시
                "content": user_input  # 실제 입력 내용
            })
            
            # Claude와의 대화 처리 루프
            # 도구 호출이 필요한 경우 여러 번 왕복할 수 있음
            while True:
                # Claude에게 메시지 전송하고 응답 받기
                response = await send_llm_request_and_display(
                    llm_client, conversation_history, anthropic_tools
                )
                
                # Claude가 도구(계산기 등)를 사용하려고 하는 경우
                if response.stop_reason == "tool_use":
                    # 도구를 실행하고 결과를 Claude에게 전달
                    await send_tool_request_and_display(
                        response, mcp_client, conversation_history
                    )
                    # 도구 결과를 받은 Claude가 최종 답변을 할 수 있도록
                    # 다시 루프를 돌아서 Claude의 응답을 기다림
                else:
                    # 도구 호출이 없으면 이번 대화 턴 종료
                    # 다음 사용자 입력을 기다림
                    break

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())