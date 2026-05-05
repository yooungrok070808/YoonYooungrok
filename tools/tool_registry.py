# tools/tool_registry.py
import io
import contextlib


def web_search(query: str) -> str:
    return f"[검색 결과] '{query}'에 대한 최신 정보가 수집되었습니다."


def run_python(code: str) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})
    return buf.getvalue() or "실행 완료 (출력 없음)"


def write_file(filename: str, content: str) -> str:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"'{filename}' 저장 완료"


TOOL_SCHEMAS = {
    "web_search": {
        "name": "web_search",
        "description": "웹에서 최신 정보를 검색합니다",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    "run_python": {
        "name": "run_python",
        "description": "Python 코드를 실행하고 결과를 반환합니다",
        "input_schema": {
            "type": "object",
            "properties": {"code": {"type": "string"}},
            "required": ["code"],
        },
    },
    "write_file": {
        "name": "write_file",
        "description": "내용을 파일로 저장합니다",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["filename", "content"],
        },
    },
}


def execute_tool(tool_name: str, tool_input: dict) -> str:
    dispatch = {
        "web_search": web_search,
        "run_python":  run_python,
        "write_file":  write_file,
    }
    fn = dispatch.get(tool_name)
    if fn is None:
        return f"[오류] 알 수 없는 도구: {tool_name}"
    return fn(**tool_input)