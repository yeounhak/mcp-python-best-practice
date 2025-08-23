import asyncio
import json
from typing import List, Dict, Any
from fastmcp import Client
from openai import AsyncOpenAI
import os

class MCPChatBot:
    def __init__(self, server_command: str, openai_api_key: str = None):
        self.server_command = server_command
        self.client = AsyncOpenAI(api_key=openai_api_key or os.getenv('OPENAI_API_KEY'))
        self.conversation_history = []
        self.available_tools = []
        
    async def initialize(self):
        """MCP 서버에 연결하고 사용 가능한 도구들을 가져옵니다."""
        self.mcp_client = Client(self.server_command)
        await self.mcp_client.__aenter__()
        
        # 사용 가능한 도구들 가져오기
        tools_response = await self.mcp_client.list_tools()
        self.available_tools = tools_response.tools
        
        print(f"🔧 사용 가능한 도구들: {[tool.name for tool in self.available_tools]}")
        
    async def cleanup(self):
        """리소스 정리"""
        if hasattr(self, 'mcp_client'):
            await self.mcp_client.__aexit__(None, None, None)
    
    def format_tools_for_openai(self) -> List[Dict[str, Any]]:
        """MCP 도구들을 OpenAI 함수 호출 형식으로 변환"""
        openai_tools = []
        for tool in self.available_tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            
            # 도구의 입력 스키마가 있다면 추가
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                if 'properties' in tool.inputSchema:
                    openai_tool["function"]["parameters"]["properties"] = tool.inputSchema['properties']
                if 'required' in tool.inputSchema:
                    openai_tool["function"]["parameters"]["required"] = tool.inputSchema['required']
            
            openai_tools.append(openai_tool)
        
        return openai_tools
    
    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """MCP 도구 호출"""
        try:
            result = await self.mcp_client.call_tool(tool_name, arguments)
            return result.content[0].text if result.content else str(result)
        except Exception as e:
            return f"도구 실행 오류: {str(e)}"
    
    async def get_llm_response(self, user_message: str) -> str:
        """OpenAI를 사용해서 응답 생성 및 도구 사용 결정"""
        
        # 시스템 메시지
        system_message = {
            "role": "system",
            "content": """당신은 도구를 사용할 수 있는 AI 어시스턴트입니다. 
사용자의 요청을 분석하고, 필요한 경우에만 적절한 도구를 사용하세요.
도구 사용이 필요하지 않은 일반적인 대화나 질문에는 직접 답변하세요."""
        }
        
        # 대화 기록에 사용자 메시지 추가
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # 전체 메시지 구성
        messages = [system_message] + self.conversation_history
        
        try:
            # OpenAI API 호출
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=self.format_tools_for_openai() if self.available_tools else None,
                tool_choice="auto"  # 자동으로 도구 사용 여부 결정
            )
            
            assistant_message = response.choices[0].message
            
            # 도구 호출이 있는지 확인
            if assistant_message.tool_calls:
                print("🤖 AI가 도구 사용을 결정했습니다...")
                
                # 각 도구 호출 실행
                tool_results = []
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 도구 실행: {tool_name} with {tool_args}")
                    
                    # MCP 도구 호출
                    tool_result = await self.call_mcp_tool(tool_name, tool_args)
                    tool_results.append(f"도구 '{tool_name}' 결과: {tool_result}")
                
                # 도구 결과를 포함해서 최종 응답 생성
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                        } for tc in assistant_message.tool_calls
                    ]
                })
                
                # 도구 결과 메시지 추가
                for i, (tool_call, result) in enumerate(zip(assistant_message.tool_calls, tool_results)):
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                
                # 도구 결과를 반영한 최종 응답 요청
                final_response = await self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[system_message] + self.conversation_history
                )
                
                final_content = final_response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": final_content})
                
                return final_content
            
            else:
                # 도구 사용 없이 직접 응답
                content = assistant_message.content
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
                
        except Exception as e:
            error_msg = f"LLM 응답 생성 오류: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    async def chat_loop(self):
        """메인 채팅 루프"""
        print("🤖 MCP ChatBot이 시작되었습니다!")
        print("💡 'quit' 또는 'exit'를 입력하면 종료됩니다.")
        print("-" * 50)
        
        while True:
            try:
                # 사용자 입력 받기
                user_input = input("\n👤 You: ").strip()
                
                # 종료 조건 확인
                if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                    print("👋 채팅을 종료합니다.")
                    break
                
                if not user_input:
                    continue
                
                # LLM 응답 생성
                print("🤔 생각 중...")
                response = await self.get_llm_response(user_input)
                print(f"\n🤖 Bot: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 채팅을 종료합니다.")
                break
            except Exception as e:
                print(f"❌ 오류 발생: {str(e)}")

async def main():
    """메인 함수"""
    # 환경 변수에서 OpenAI API 키 확인
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY 환경 변수를 설정해주세요.")
        return
    
    # MCP 서버 명령어 (예: "server.py" 또는 실제 서버 경로)
    server_command = "server.py"  # 실제 MCP 서버 경로로 변경하세요
    
    # ChatBot 인스턴스 생성
    chatbot = MCPChatBot(server_command)
    
    try:
        # 초기화
        await chatbot.initialize()
        
        # 채팅 시작
        await chatbot.chat_loop()
        
    except Exception as e:
        print(f"❌ ChatBot 실행 오류: {str(e)}")
    finally:
        # 정리
        await chatbot.cleanup()

if __name__ == '__main__':
    # 사용법 예시
    print("""
    🚀 MCP ChatBot 사용법:
    
    1. OpenAI API 키 설정:
       export OPENAI_API_KEY="your-api-key-here"
    
    2. MCP 서버 준비:
       - server.py 파일이나 실제 MCP 서버가 준비되어 있어야 합니다.
    
    3. 필요한 패키지 설치:
       pip install fastmcp openai
    
    4. 실행:
       python mcp_chatbot.py
    """)
    
    asyncio.run(main())