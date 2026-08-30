from openai import OpenAI
from agent.config import OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

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