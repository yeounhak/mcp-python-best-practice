from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print(f"\nAvailable tools: {tools}")
        
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"\nResult: {result}")
        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
