from app.models import TaskOutput

import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
import logfire
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP


load_dotenv()


mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8080/sse')
server = MCPServerHTTP(url=mcp_server_url)  



agent = Agent(
    model='anthropic:claude-3-7-sonnet-20250219',
    result_type=TaskOutput,
    mcp_servers = [server],
    system_prompt='use mcp server to find info of database',
    instrument=False,
)

async def generate_task(prompt: str) -> TaskOutput:
    async with agent.run_mcp_servers():
        result = await agent.run(prompt)
        return result.data
