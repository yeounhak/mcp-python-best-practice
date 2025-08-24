from fastmcp import Client

async def main():
    # MCP 서버에 연결
    async with Client("http://0.0.0.0:9000/mcp") as client:
        resources = await client.list_resources()
        print(f"✅ {len(resources)}개의 리소스를 찾았습니다.\n")
        
        # 각 리소스의 내용을 읽어서 출력
        for i, resource in enumerate(resources, 1):
            print(f"\n📄 [{i}] Resource URI: {resource}")
            
            content = await client.read_resource(resource.uri)
            print(f"📝 Content: {content}")

        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())