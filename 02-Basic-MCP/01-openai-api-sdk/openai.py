from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key = "sk-..."
)

async def main():
    stream = await client.chat.completions.create(
        model="gpt-5",
        messages=[{"role":"assistant", "content": "hi"}],
        stream=True
    )
    async for chunk in stream:
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())