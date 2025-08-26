from anthropic import AsyncAnthropic

client = AsyncAnthropic(
    api_key="sk-ant-..."
)

async def main():
    stream = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=1024,
        stream=True
    )
    async for chunk in stream:
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())