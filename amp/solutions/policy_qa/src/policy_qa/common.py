"""Shared settings: the model and the workshop data connector.

You don't need to edit this file. On AMP, your deployment gets OPENAI_API_KEY from an
organization variable you link to it, so the key never appears in your project."""
import os

from crewai import LLM
from crewai.mcp import MCPServerHTTP

# Northwind Auto Finance sample data: 15 policies, an intake inbox and customer accounts.
DATA_CONNECTOR_URL = "https://d3m5dyfy6s31ka.cloudfront.net/mcp"


def llm() -> LLM:
    return LLM(model=os.environ.get("MODEL", "openai/gpt-6-luna"))


def connector() -> MCPServerHTTP:
    """The Northwind Workshop Data connector (search_policies, get_policy, ...)."""
    return MCPServerHTTP(url=os.environ.get("MCP_URL", DATA_CONNECTOR_URL))
