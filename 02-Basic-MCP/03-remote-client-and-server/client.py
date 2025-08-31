from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("http://localhost:8000/mcp") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())