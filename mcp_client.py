import os

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from pydantic_ai.mcp import MCPToolset


def make_toolset(command: str, args: list[str], github_token: str):
    if not github_token:
        raise RuntimeError(
            "GITHUB_PERSONAL_ACCESS_TOKEN is missing. "
            "Add it to your .env file."
        )

    env = os.environ.copy()
    env["GITHUB_PERSONAL_ACCESS_TOKEN"] = github_token

    transport = StdioTransport(
        command=command,
        args=args,
        env=env,
    )

    client = Client(transport)

    return MCPToolset(
        client,
        include_instructions=True,
    )