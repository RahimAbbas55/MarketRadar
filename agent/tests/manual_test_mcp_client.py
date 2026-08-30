import asyncio
import os
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "agent.mcp_server"],
    cwd=os.getcwd(),
    env=os.environ.copy()
)

async def run():
    async with stdio_client(SERVER_PARAMS, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\nCalling fetch_technical_indicators for TSLA...")
            result = await session.call_tool("fetch_technical_indicators", {"ticker": "TSLA"})
            print(result.content[0].text)

            print("\nCalling compare_stocks for TSLA vs RIVN...")
            comparison_result = await session.call_tool(
                "compare_stocks",
                {"tickers": ["TSLA", "RIVN"]}
            )
            parsed = json.loads(comparison_result.content[0].text)
            print(json.dumps(parsed, indent=2))

if __name__ == "__main__":
    asyncio.run(run())