"""Shared settings: which model to use and where the workshop data connector lives.

Both come from the .env file in the repo root (copied from .env.example)."""
import os

from crewai import LLM
from crewai.mcp import MCPServerHTTP

DEFAULT_MCP_URL = "https://d3m5dyfy6s31ka.cloudfront.net/mcp"


def llm() -> LLM:
    return LLM(model=os.environ.get("MODEL", "openai/gpt-6-luna"))


def connector() -> MCPServerHTTP:
    """The Northwind Auto Finance data connector (policies, inbox, accounts)."""
    return MCPServerHTTP(url=os.environ.get("MCP_URL", DEFAULT_MCP_URL))
