from fastmcp import Client

from anthropic import AsyncAnthropic

async def main():
    llm_client = AsyncAnthropic()
    
    # 시스템 메시지
    conversation_history = []
    
    async with Client("server.py") as mcp_client:
        available_tools = await mcp_client.list_tools()
        anthropic_tools = []
        for tool in available_tools:
            anthropic_tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
            })


        user_input = input("👤 User: ")
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        response = await llm_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=conversation_history,
            tools=anthropic_tools,
        )
        
        # Add assistant response to conversation
        conversation_history.append({
            "role": "assistant",
            "content": response.content
        })
        for content_block in response.content:
            if content_block.type == "text":
                print("[🤖 Assistant:]", content_block.text)
        
        # Check if tool calls are needed
        if response.stop_reason == "tool_use":
            tool_results = []
            
            for content_block in response.content:
                if content_block.type == "tool_use":
                    print(f"[🔧 Tool Request] {content_block.name}({content_block.input})")
                    
                    # Execute the tool call
                    tool_result = await mcp_client.call_tool(
                        content_block.name, 
                        content_block.input
                    )
                    
                    print(f"[✅ Tool Result] {tool_result}")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": str(tool_result)
                    })
            
            # Add tool results to conversation
            conversation_history.append({
                "role": "user",
                "content": tool_results
            })
            
            # Get final response after tool execution
            final_response = await llm_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=conversation_history,
                tools=anthropic_tools,
            )
            
            conversation_history.append({
                "role": "assistant",
                "content": final_response.content
            })
            
            # Display final response
            for content_block in final_response.content:
                if content_block.type == "text":
                    print("[🤖 Assistant:]", content_block.text)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())