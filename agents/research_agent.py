# agents/research_agent.py
import anthropic
from tools.tool_registry import TOOL_SCHEMAS, execute_tool

client = anthropic.Anthropic()


def run_research_agent(task: str) -> str:
    tools = [TOOL_SCHEMAS["web_search"]]
    messages = [{"role": "user", "content": task}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system="당신은 정보 수집 전문 에이전트입니다. 주어진 주제를 철저히 조사하세요.",
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return next(b.text for b in response.content if hasattr(b, "text"))

        messages.append({"role": "assistant", "content": response.content})
        results = []

        for block in response.content:
            if block.type == "tool_use":
                print(f"    [Research] {block.name}({block.input})")
                result = execute_tool(block.name, block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

        messages.append({"role": "user", "content": results})