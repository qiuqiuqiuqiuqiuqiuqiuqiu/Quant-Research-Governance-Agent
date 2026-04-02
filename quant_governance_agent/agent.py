"""The whole agent kernel: model → tools → evidence → model, bounded and auditable."""
from __future__ import annotations
import inspect
from .audit import AuditLog
from .context import ContextManager
from .prompt import system_prompt

class Agent:
    def __init__(self, llm, tools, workspace, audit_log, max_context_tokens=64_000, max_rounds=30):
        self.llm, self.tools, self.workspace = llm, tools, workspace
        self.messages, self.max_rounds = [], max_rounds
        self.by_name = {tool.name: tool for tool in tools}
        self.audit, self.context = AuditLog(audit_log), ContextManager(max_context_tokens)
        self.system = system_prompt(workspace, tools)

    def chat(self, user_input: str, on_token=None, on_tool=None) -> str:
        self.messages.append({"role": "user", "content": user_input})
        self.audit.record("user_request", content=user_input)
        for round_number in range(1, self.max_rounds + 1):
            self.context.maybe_compress(self.messages)
            response = self.llm.chat([{"role": "system", "content": self.system}, *self.messages], [t.schema() for t in self.tools], on_token)
            self.messages.append(response.message)
            if not response.tool_calls:
                self.audit.record("final_response", round=round_number, content=response.content)
                return response.content
            for call in response.tool_calls:
                if on_tool: on_tool(call.name, call.arguments)
                result = self._execute(call.name, call.arguments)
                self.messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
                self.audit.record("tool_call", round=round_number, tool=call.name, arguments=call.arguments, result=result)
        outcome = "[Stopped: maximum tool rounds reached; human review required.]"
        self.audit.record("agent_stopped", reason="max_rounds")
        return outcome

    def _execute(self, name, arguments) -> str:
        tool = self.by_name.get(name)
        if not tool: return f"Error: unknown tool '{name}'"
        try: inspect.signature(tool.execute).bind(**arguments)
        except TypeError as exc: return f"Error: invalid arguments for {name}: {exc}"
        try: return tool.execute(**arguments)
        except Exception as exc: return f"Error executing {name}: {exc}"
