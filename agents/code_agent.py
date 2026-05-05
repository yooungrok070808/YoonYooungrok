# agents/code_agent.py
import anthropic
from tools.tool_registry import TOOL_SCHEMAS, execute_tool

client = anthropic.Anthropic()


def run_code_agent(task: str) -> str:
    tools = [TOOL_SCHEMAS["run_python"], TOOL_SCHEMAS["write_file"]]
    messages = [{"role": "user", "content": task}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system="당신은 Python 코드 작성·실행 전문 에이전트입니다. print()로 결과를 출력하세요.",
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return next(b.text for b in response.content if hasattr(b, "text"))

        messages.append({"role": "assistant", "content": response.content})
        results = []

        for block in response.content:
            if block.type == "tool_use":
                print(f"    [Code] {block.name}")
                result = execute_tool(block.name, block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

        messages.append({"role": "user", "content": results})