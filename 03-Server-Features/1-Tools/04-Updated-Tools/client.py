from fastmcp import Client

async def message_handler(message):
    """서버로부터 오는 모든 MCP 메시지를 처리합니다."""
    if hasattr(message, 'root'):
        method = message.root.method
        print(f"📨 수신됨: {method}")
        
        # 특정 알림 처리
        if method == "notifications/tools/list_changed":
            print("🔄 도구가 변경되어 list_tools를 다시 호출하세요")


async def main():
    async with Client(
            transport_url="http://localhost:9000",
            message_handler=message_handler,
        ) as client:
        tools = await client.list_tools()
        print(f"\n🛠️ 사용 가능한 도구: {[tool.name for tool in tools]}")
        
        result = await client.call_tool("hello_tool")
        print(f"\n✅ 결과: {result}")
        
        # hello_tool 호출 후 도구가 변경되었는지 확인
        tools_after = await client.list_tools()
        print(f"\n🔍 hello_tool 실행 후 사용 가능한 도구: {[tool.name for tool in tools_after]}")
        
        result = await client.call_tool("add_tool", {"a": 5, "b": 3})
        print(f"\n✅ 결과: {result}")
        
        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
