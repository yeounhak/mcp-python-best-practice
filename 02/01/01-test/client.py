from fastmcp import Client

from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.messages import SystemMessage, HumanMessage
# from openai import AsyncOpenAI
# llm_client = AsyncOpenAI()
from anthropic import AsyncAnthropic
llm_client = AsyncAnthropic()

from anthropic import AsyncAnthropic

async def main():
    # 시스템 메시지
    conversation_history = [
        SystemMessage(content="당신은 AI 어시스턴트입니다.")
    ]
    async with Client("server.py") as mcp_client:
        available_tools = await mcp_client.list_tools()
        anthropic_tools = []
        for tool in available_tools:
            anthropic_tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
            })

        while True:
            conversation_history.append(
                HumanMessage(content=input())
            )
            response = await llm_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=conversation_history,
                tools=anthropic_tools,
            )

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())