import aiofiles
import asyncio
import time
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

@mcp.resource("file://log.txt", mime_type="text/plain")
async def aiofiles_resource() -> str:
    """Reads content from a specific log file asynchronously."""
    try:
        async with aiofiles.open("log.txt", mode="r") as f:
            content = await f.read()
        await asyncio.sleep(1)
        return content
    except FileNotFoundError:
        return "Log file not found."

@mcp.resource("file://log-sync.txt", mime_type="text/plain")
async def open_resource() -> str:
    """Reads content from a specific log file using standard open() in async function."""
    try:
        with open("log.txt", "r") as f:
            content = f.read()
        time.sleep(1)
        return content
    except FileNotFoundError:
        return "Log file not found."

mcp.run(transport="http", port=9000)