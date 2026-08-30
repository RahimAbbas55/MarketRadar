import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agent.core.llm_agent import run_agent, mcp_tools_to_openai_schema

SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "agent.mcp_server"],
    cwd=os.getcwd(),
    env=os.environ.copy()
)

TEST_QUESTIONS = [
    "What is Tesla's current RSI, and is it overbought or oversold?",
    "Compare Tesla and Rivian on volatility and recent news sentiment. Which looks riskier right now?"
]

async def run():
    async with stdio_client(SERVER_PARAMS, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            openai_tools = mcp_tools_to_openai_schema(tools.tools)

            for question in TEST_QUESTIONS:
                print(f"Question: {question}\n")
                answer = await run_agent(question, session, openai_tools)
                print(f"Answer: {answer}\n")
                print("-" * 80)

if __name__ == "__main__":
    asyncio.run(run())