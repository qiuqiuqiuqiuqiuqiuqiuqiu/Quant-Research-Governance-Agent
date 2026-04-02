import argparse
from .config import Config
from .llm import LLM
from .agent import Agent
from .tools import default_tools

def main():
    parser = argparse.ArgumentParser(description="Quant Research & Governance Agent")
    parser.add_argument("-p", "--prompt", required=True, help="One-shot governance task")
    args = parser.parse_args()
    config = Config.from_env()
    if not config.api_key:
        parser.error("Set QUANT_AGENT_API_KEY or OPENAI_API_KEY")
    agent = Agent(LLM(config.model, config.api_key, config.base_url, max_tokens=config.max_tokens), default_tools(config.workspace), config.workspace, config.audit_log, config.max_context_tokens, config.max_rounds)
    print(agent.chat(args.prompt))
