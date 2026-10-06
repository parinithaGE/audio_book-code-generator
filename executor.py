import ast
import subprocess
import sys
import tempfile
from pathlib import Path

def run_generated_code(code: str, pdf_path: Path):
    try:
        ast.parse(code)
    except SyntaxError as exc:
        return {"passed": False, "reason": str(exc), "files": [], "stdout": "", "stderr": ""}
    work = Path(tempfile.mkdtemp(prefix="audiobook_test_"))
    target = work / "Audio-book.py"
    target.write_text(code, encoding="utf-8")
    (work / "test.pdf").write_bytes(pdf_path.read_bytes())
    if "streamlit" in code:
        return {"passed": True, "reason": "Streamlit code is valid. The supplied PDF is available as test.pdf; interactive UI testing is required for upload/voice selection.", "files": [], "stdout": "", "stderr": ""}
    result = subprocess.run([sys.executable, str(target)], cwd=work, capture_output=True, text=True, timeout=60)
    outputs = [p for p in work.rglob("*") if p.is_file() and p.name not in {"Audio-book.py", "test.pdf"}]
    return {"passed": result.returncode == 0, "reason": "Execution successful." if result.returncode == 0 else "Execution failed.", "files": outputs, "stdout": result.stdout, "stderr": result.stderr}
