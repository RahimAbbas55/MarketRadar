import json
from openai import OpenAI
from agent.config import OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-4o"
MAX_ITERATIONS = 5

SYSTEM_PROMPT = (
    "You are MarketRadar, an investment research assistant. "
    "Use the available tools to fetch real data before answering. "
    "Never guess numbers. If a tool returns an error, mention it plainly to the user."
)

# Converts MCP tool definitions into the schema format OpenAI's function calling expects
def mcp_tools_to_openai_schema(mcp_tools: list) -> list[dict]:
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })
    return openai_tools

# Core agent loop: LLM decides tool calls, we execute via MCP, feed results back, repeat
async def run_agent(user_message: str, session, openai_tools: list[dict]) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=openai_tools
        )
        choice = response.choices[0]
        messages.append(choice.message)
        if not choice.message.tool_calls:
            return choice.message.content
        for tool_call in choice.message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            result = await session.call_tool(tool_name, tool_args)
            tool_output = result.content[0].text
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_output
            })

    return "I wasn't able to complete this request within the allowed number of steps."