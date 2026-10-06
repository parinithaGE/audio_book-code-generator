from pydantic_ai import Agent
from src.llm import build_model

def generate_code(base_url, model_name, original_code, feature_request):
    agent = Agent(
        build_model(base_url, model_name),
        instructions="""
Modify the existing Python audiobook file according to the user's request.
Return ONLY complete Python source code.
Do not return Markdown or explanations.
Preserve existing functionality.
Do not invent pip packages or library parameters.
Do not use tkinter or tkfiledialog.
Every imported module must be valid and imported.
The result must be valid executable Python.
If a UI is needed, use Streamlit.
A local test PDF named test.pdf will be available during testing.
If male/female voice selection is requested, use a real TTS engine with selectable voices; never invent a gTTS voice parameter.
""",
    )
    result = agent.run_sync(f"Existing file:\n{original_code}\n\nUser request:\n{feature_request}\n\nReturn only the complete modified Python source code.")
    code = result.output.strip()
    if code.startswith("```"):
        lines = code.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines).strip()
    if not code:
        raise RuntimeError("AI returned empty code.")
    return code
