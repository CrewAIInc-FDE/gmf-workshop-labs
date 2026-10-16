"""Shared settings: the model and the workshop data connector.

You don't need to edit this file. On AMP, your deployment gets OPENAI_API_KEY from an
organization variable you link to it, so the key never appears in your project."""
import os

from crewai import LLM
from crewai.mcp import MCPServerHTTP, create_static_tool_filter

# Northwind Auto Finance sample data: 15 policies, an intake inbox and 50 customer accounts.
DATA_CONNECTOR_URL = "https://d3m5dyfy6s31ka.cloudfront.net/mcp"


def llm() -> LLM:
    return LLM(model=os.environ.get("MODEL", "openai/gpt-6-luna"))


def connector(*tool_names: str) -> MCPServerHTTP:
    """The Northwind Workshop Data connector. Name the tools an agent may use (for example
    get_client_account); with no names, the agent gets every tool the connector offers."""
    return MCPServerHTTP(
        url=os.environ.get("MCP_URL", DATA_CONNECTOR_URL),
        tool_filter=create_static_tool_filter(allowed_tool_names=list(tool_names)) if tool_names else None,
    )
