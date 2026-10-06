import os

from dotenv import load_dotenv

load_dotenv()


REPO = "https://github.com/Python-World/python-mini-projects"
TARGET = "projects/AudioBook/Audio-book.py"


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv(
    "GITHUB_PERSONAL_ACCESS_TOKEN",
    ""
)

MCP_COMMAND = os.getenv(
    "MCP_COMMAND",
    "github-mcp-server"
)

MCP_ARGS = os.getenv(
    "MCP_ARGS",
    "stdio --read-only"
).split()