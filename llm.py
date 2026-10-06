from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

def build_model(base_url: str, model_name: str):
    base_url = base_url.rstrip("/")
    if not base_url.endswith("/v1"):
        base_url += "/v1"
    provider = OpenAIProvider(base_url=base_url, api_key="ollama")
    return OpenAIChatModel(model_name, provider=provider)

def build_agent(base_url, model_name, instructions, toolsets=None):
    return Agent(build_model(base_url, model_name), instructions=instructions, toolsets=toolsets or [])
