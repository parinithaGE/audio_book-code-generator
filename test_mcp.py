import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StdioTransport


load_dotenv()


async def main():
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

    if not token:
        raise RuntimeError(
            "GITHUB_PERSONAL_ACCESS_TOKEN is missing from .env"
        )

    env = os.environ.copy()
    env["GITHUB_PERSONAL_ACCESS_TOKEN"] = token

    transport = StdioTransport(
        command="github-mcp-server",
        args=["stdio", "--read-only"],
        env=env,
    )

    client = Client(transport)

    print("Connecting to GitHub MCP...")

    async with client:
        print("MCP connection successful.")

        tools = await client.list_tools()

        print(f"Found {len(tools)} MCP tools.")

        for tool in tools:
            print("-", tool.name)


if __name__ == "__main__":
    asyncio.run(main())