import os
import sys
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agent.core.llm_agent import mcp_tools_to_openai_schema, run_agent, run_agent_streaming
from fastapi.middleware.cors import CORSMiddleware

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

            yield  # app runs here, handling requests

    # shutdown: the async with blocks above close the session automatically on exit
    mcp_state.clear()

app = FastAPI(title="MarketRadar API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    answer = await run_agent(
        request.message,
        mcp_state["session"],
        mcp_state["openai_tools"]
    )
    return ChatResponse(answer=answer)

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        async for event in run_agent_streaming(
            request.message,
            mcp_state["session"],
            mcp_state["openai_tools"]
        ):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")