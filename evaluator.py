import ast
from pydantic_ai import Agent
from src.llm import build_model

def evaluate_code(base_url, model_name, code, request, pass_number):
    if pass_number == 2:
        try:
            ast.parse(code)
            return True, "Pass 2: Python syntax is valid."
        except SyntaxError as exc:
            return False, f"Pass 2 failed: {exc}"
    agent = Agent(
        build_model(base_url, model_name),
        instructions="Return exactly one line beginning with PASS or FAIL, followed by a short reason. Do not rewrite the code.",
    )
    result = agent.run_sync(f"Pass: {pass_number}\nUser request:\n{request}\n\nCode:\n{code}\n\nCheck whether the code satisfies this evaluation pass.")
    text = result.output.strip()
    return text.upper().startswith("PASS"), text
