from fastmcp import FastMCP, Context
import asyncio
import time

mcp = FastMCP(name="ContextDemo")

@mcp.tool
async def demonstrate_logging(message: str, ctx: Context) -> dict:
    """Demonstrate all logging levels with Context."""
    
    # Different logging levels
    await ctx.debug(f"Debug: Processing message '{message}'")
    await ctx.info(f"Info: Starting to process message")
    await ctx.warning(f"Warning: This is just a demo warning")
    await ctx.error(f"Error: This is just a demo error (not a real error)")
    
    # Access request information
    request_info = {
        "request_id": ctx.request_id,
        "client_id": ctx.client_id
    }
    
    await ctx.info(f"Request info: {request_info}")
    
    return {
        "message": f"Processed: {message}",
        "request_info": request_info,
        "logging_complete": True
    }

@mcp.tool
async def process_with_progress(task_name: str, steps: int, ctx: Context) -> dict:
    """Demonstrate progress reporting during task execution."""
    
    await ctx.info(f"Starting task: {task_name} with {steps} steps")
    
    results = []
    for i in range(steps):
        # Report progress
        progress = i + 1
        await ctx.report_progress(progress=progress, total=steps)
        
        # Simulate work
        await asyncio.sleep(0.5)
        
        step_result = f"Step {progress}/{steps}: Processing..."
        results.append(step_result)
        
        await ctx.debug(f"Completed step {progress}")
    
    await ctx.info(f"Task '{task_name}' completed successfully!")
    
    return {
        "task_name": task_name,
        "total_steps": steps,
        "results": results,
        "status": "completed"
    }

@mcp.tool
async def analyze_data_with_llm(data: str, analysis_type: str, ctx: Context) -> dict:
    """Demonstrate LLM sampling for data analysis."""
    
    await ctx.info(f"Starting {analysis_type} analysis of data")
    await ctx.report_progress(progress=25, total=100)
    
    # Different types of analysis using LLM sampling
    if analysis_type == "summary":
        prompt = f"Summarize this text in exactly 15 words: {data[:500]}"
    elif analysis_type == "sentiment":
        prompt = f"Analyze the sentiment of this text (positive/negative/neutral) and explain briefly: {data[:300]}"
    elif analysis_type == "keywords":
        prompt = f"Extract 5 key topics/keywords from this text: {data[:400]}"
    else:
        prompt = f"Analyze this text and provide insights: {data[:200]}"
    
    await ctx.report_progress(progress=50, total=100)
    await ctx.info("Requesting LLM analysis...")
    
    try:
        # Request analysis from client's LLM
        response = await ctx.sample(prompt)
        analysis_result = response.text
        
        await ctx.report_progress(progress=100, total=100)
        await ctx.info("Analysis completed successfully")
        
        return {
            "analysis_type": analysis_type,
            "data_length": len(data),
            "analysis_result": analysis_result,
            "status": "success"
        }
        
    except Exception as e:
        await ctx.error(f"LLM analysis failed: {str(e)}")
        return {
            "analysis_type": analysis_type,
            "data_length": len(data),
            "error": str(e),
            "status": "failed"
        }

@mcp.tool
async def read_and_process_resource(resource_uri: str, ctx: Context) -> dict:
    """Demonstrate resource reading and processing."""
    
    await ctx.info(f"Attempting to read resource: {resource_uri}")
    
    try:
        # Read resource
        resources = await ctx.read_resource(resource_uri)
        
        if not resources:
            await ctx.warning("No resources found for the given URI")
            return {
                "resource_uri": resource_uri,
                "status": "not_found",
                "content": None
            }
        
        # Process first resource
        resource = resources[0]
        content = resource.content
        
        await ctx.info(f"Resource read successfully, content length: {len(content)}")
        await ctx.report_progress(progress=50, total=100)
        
        # Analyze content
        word_count = len(content.split()) if isinstance(content, str) else 0
        char_count = len(content) if content else 0
        
        await ctx.report_progress(progress=100, total=100)
        await ctx.info("Resource processing completed")
        
        return {
            "resource_uri": resource_uri,
            "status": "success",
            "content_preview": content[:200] if content else "",
            "word_count": word_count,
            "char_count": char_count,
            "resource_type": type(content).__name__
        }
        
    except Exception as e:
        await ctx.error(f"Failed to read resource: {str(e)}")
        return {
            "resource_uri": resource_uri,
            "status": "error",
            "error": str(e)
        }

@mcp.tool
async def comprehensive_demo(input_text: str, ctx: Context) -> dict:
    """Comprehensive demonstration of all Context features."""
    
    demo_start = time.time()
    
    # Step 1: Logging
    await ctx.info("=== Comprehensive Context Demo Started ===")
    await ctx.debug(f"Input text length: {len(input_text)}")
    await ctx.report_progress(progress=10, total=100)
    
    # Step 2: Request information
    request_info = {
        "request_id": ctx.request_id,
        "client_id": ctx.client_id,
        "timestamp": demo_start
    }
    await ctx.info(f"Request details: {request_info}")
    await ctx.report_progress(progress=25, total=100)
    
    # Step 3: LLM Analysis
    await ctx.info("Performing LLM analysis...")
    try:
        summary_response = await ctx.sample(f"Create a brief summary of this text: {input_text[:300]}")
        summary = summary_response.text
        await ctx.info("LLM analysis completed")
    except Exception as e:
        await ctx.warning(f"LLM analysis failed: {e}")
        summary = "Analysis unavailable"
    
    await ctx.report_progress(progress=60, total=100)
    
    # Step 4: Processing simulation
    await ctx.info("Simulating data processing...")
    await asyncio.sleep(1)  # Simulate processing time
    
    processed_data = {
        "original_length": len(input_text),
        "word_count": len(input_text.split()),
        "summary": summary,
        "processing_time": time.time() - demo_start
    }
    
    await ctx.report_progress(progress=90, total=100)
    
    # Step 5: Final results
    final_result = {
        "demo_status": "completed",
        "request_info": request_info,
        "processed_data": processed_data,
        "context_features_used": [
            "logging (debug, info, warning)",
            "progress_reporting",
            "llm_sampling",
            "request_information"
        ]
    }
    
    await ctx.report_progress(progress=100, total=100)
    await ctx.info("=== Comprehensive Context Demo Completed ===")
    
    return final_result

if __name__ == "__main__":
    mcp.run(transport='http')