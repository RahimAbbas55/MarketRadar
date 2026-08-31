import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agent.core.llm_agent import mcp_tools_to_openai_schema

SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "agent.mcp_server"],
    cwd=os.getcwd(),
    env=os.environ.copy()
)

mcp_state = {}

# startup: open the MCP session once and keep it alive for the app's lifetime
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with stdio_client(SERVER_PARAMS, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()

            mcp_state["session"] = session
            mcp_state["openai_tools"] = mcp_tools_to_openai_schema(tools.tools)

            yield

    # shutdown: the async with blocks above close the session automatically on exit
    mcp_state.clear()

app = FastAPI(title="MarketRadar API", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}