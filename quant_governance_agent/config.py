"""Configuration from environment variables; deliberately small and explicit."""
from dataclasses import dataclass
import os
from pathlib import Path

@dataclass
class Config:
    model: str = "gpt-4.1-mini"
    api_key: str = ""
    base_url: str | None = None
    max_tokens: int = 4096
    max_context_tokens: int = 64_000
    max_rounds: int = 30
    workspace: Path = Path.cwd()
    audit_log: Path = Path(".quant-agent/audit.jsonl")

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            model=os.getenv("QUANT_AGENT_MODEL", "gpt-4.1-mini"),
            api_key=os.getenv("QUANT_AGENT_API_KEY") or os.getenv("OPENAI_API_KEY", ""),
            base_url=os.getenv("QUANT_AGENT_BASE_URL") or os.getenv("OPENAI_BASE_URL"),
            max_tokens=int(os.getenv("QUANT_AGENT_MAX_TOKENS", "4096")),
            max_context_tokens=int(os.getenv("QUANT_AGENT_MAX_CONTEXT", "64000")),
            max_rounds=int(os.getenv("QUANT_AGENT_MAX_ROUNDS", "30")),
            workspace=Path(os.getenv("QUANT_AGENT_WORKSPACE", Path.cwd())).resolve(),
            audit_log=Path(os.getenv("QUANT_AGENT_AUDIT_LOG", ".quant-agent/audit.jsonl")),
        )
