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

def mcp_tools_to_openai_schema(mcp_tools: list) -> list[dict]:
    # converts MCP tool definitions into the schema format OpenAI's function calling expects
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

async def run_agent(user_message: str, session, openai_tools: list[dict]) -> str:
    # core agent loop: LLM decides tool calls, we execute via MCP, feed results back, repeat
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    for iteration in range(MAX_ITERATIONS):
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

            try:
                tool_args = json.loads(tool_call.function.arguments)
                result = await session.call_tool(tool_name, tool_args)
                tool_output = result.content[0].text
            except Exception as e:
                tool_output = json.dumps({"error": f"Tool '{tool_name}' failed to execute: {e}"})

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_output
            })

    return (
        "I wasn't able to complete this request within the allowed number of steps. "
        "This might mean the question needs to be broken down into smaller parts."
    )

async def run_agent_streaming(user_message: str, session, openai_tools: list[dict]):
    # same agent loop as run_agent, but yields progress events instead of returning once at the end
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    for iteration in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=openai_tools
        )

        choice = response.choices[0]
        messages.append(choice.message)

        if not choice.message.tool_calls:
            yield {"type": "final_answer", "content": choice.message.content}
            return

        for tool_call in choice.message.tool_calls:
            tool_name = tool_call.function.name
            yield {"type": "tool_call", "tool": tool_name}

            try:
                tool_args = json.loads(tool_call.function.arguments)
                result = await session.call_tool(tool_name, tool_args)
                tool_output = result.content[0].text
            except Exception as e:
                tool_output = json.dumps({"error": f"Tool '{tool_name}' failed to execute: {e}"})

            yield {"type": "tool_result", "tool": tool_name, "content": tool_output}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_output
            })

    yield {"type": "final_answer", "content": "I wasn't able to complete this request within the allowed number of steps."}