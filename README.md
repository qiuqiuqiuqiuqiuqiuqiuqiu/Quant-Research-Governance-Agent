# Quant Research & Governance Agent

一个受 [CoreCoder](CoreCoder/README_CN.md) 启发的最小可读框架：保留其精髓——**有上限的 agent 循环、明确工具边界、上下文预算、可替换 LLM、可审计状态**——并把工具替换为量化研究与治理能力。

## 设计目标

- **研究闭环**：登记假设、数据血缘、方法与复现命令，再记录回测证据。
- **治理优先**：确定性校验缺失指标和风险阈值；校验通过仍只是 `validated_pending_approval`，绝不等同上线。
- **人类在环**：`request_approval` 只能创建人工审批请求，框架没有部署工具。
- **审计可追溯**：用户请求、工具参数和结果追加到 `.quant-agent/audit.jsonl`。
- **小而可 fork**：核心循环在 `agent.py`，工具以 JSON Schema 暴露，离线 `ScriptedLLM` 便于测试。

## 架构

```text
用户任务 → LLM 规划 → 研究/治理工具 → 证据与审计日志 → LLM 结论
                 ↑                 │
                 └──── 有轮次上限 ──┘
```

```text
quant_governance_agent/
├── agent.py       有界 tool-use 主循环
├── llm.py         OpenAI 兼容接口 + 离线 ScriptedLLM
├── context.py     三档上下文压缩
├── audit.py       追加式 JSONL 审计
├── prompt.py      研究、风险和审批约束
└── tools/
    ├── research.py    研究登记、回测证据
    └── governance.py  校验与人工审批请求
```

## 快速开始

```bash
python -m pip install -e '.[openai]'
export OPENAI_API_KEY=sk-...
quant-governance -p '登记一个均值回归研究，补齐数据血缘和复现命令，然后说明所需治理证据。'
pytest -q
```

可用工具：`register_research`、`record_backtest`、`validate_research`、`request_approval`。所有状态写入工作目录下 `.quant-agent/`，可纳入受控的研究档案系统。

## 核心原则

该框架提供研究和治理工作流骨架，不构成投资建议，也不应直接连接生产交易或部署权限。生产使用应另外接入身份认证、审批签名、数据权限、不可篡改日志、风险限额和隔离执行环境。
