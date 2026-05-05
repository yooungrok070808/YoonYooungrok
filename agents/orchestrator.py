# agents/orchestrator.py
import anthropic
from agents.research_agent import run_research_agent
from agents.code_agent import run_code_agent

client = anthropic.Anthropic()

SUBAGENT_SCHEMAS = [
    {
        "name": "call_research_agent",
        "description": "정보 수집이 필요할 때 Research 에이전트에 위임합니다",
        "input_schema": {
            "type": "object",
            "properties": {"task": {"type": "string"}},
            "required": ["task"],
        },
    },
    {
        "name": "call_code_agent",
        "description": "코드 작성·실행이 필요할 때 Code 에이전트에 위임합니다",
        "input_schema": {
            "type": "object",
            "properties": {"task": {"type": "string"}},
            "required": ["task"],
        },
    },
]

SUBAGENT_MAP = {
    "call_research_agent": run_research_agent,
    "call_code_agent": run_code_agent,
}


def run_orchestrator(user_request: str) -> str:
    messages = [{"role": "user", "content": user_request}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=(
                "당신은 총괄 오케스트레이터입니다.\n"
                "- 정보·조사 → call_research_agent\n"
                "- 코드 작성/실행 → call_code_agent"
            ),
            tools=SUBAGENT_SCHEMAS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return next(b.text for b in response.content if hasattr(b, "text"))

        messages.append({"role": "assistant", "content": response.content})
        results = []

        for block in response.content:
            if block.type == "tool_use":
                print(f"  [Orchestrator] → {block.name}: {block.input['task'][:50]}...")
                fn = SUBAGENT_MAP.get(block.name)
                result = fn(block.input["task"]) if fn else f"[오류] {block.name} 없음"
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

        messages.append({"role": "user", "content": results})