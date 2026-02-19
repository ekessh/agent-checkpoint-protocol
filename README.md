# AgentStateProtocol — Decision State Infrastructure for Regulated AI

**An open-source checkpointing and recovery protocol for AI agents**

> Capture, replay, and audit every step of an AI agent's reasoning chain. When a model hits a failure, it recovers to the last valid state and continues — without starting over. When a decision is challenged, you can replay exactly how it was reached.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Package](https://img.shields.io/badge/PyPI-agentstateprotocol-blue.svg)](https://pypi.org/project/agentstateprotocol/)

---

## The Problem

Modern AI agents make high-stakes decisions — loan approvals, claim denials, triage suggestions, fraud alerts — but leave behind no replayable record of how they got there. When something goes wrong:

- Logs show **inputs and outputs**, not the reasoning path
- Multi-step failures force a **full restart**, losing all intermediate state
- There is **no forensic trail** for compliance, audit, or legal challenge
- Developers **can't see where hallucination entered** the chain

This isn't a developer experience problem. It's a **reliability and governance gap** that blocks enterprise adoption of agentic AI.

## The Approach

AgentStateProtocol gives your agent a versioned reasoning timeline:

| Git Concept | Agent Equivalent | Why It Helps |
|---|---|---|
| `git commit` | `agent.checkpoint()` | Save state at important points |
| `git reset` | `agent.rollback()` | Recover from bad or failed steps |
| `git branch` | `agent.branch()` | Explore alternative strategies safely |
| `git merge` | `agent.merge()` | Bring winning branch outcomes back |
| `git log` | `agent.history()` | Inspect decision history |
| `git diff` | `agent.diff()` | Compare state transitions |

---

## Why This Matters: Mission-Critical Use Cases

Checkpointing is not a convenience feature. In the following domains, it is **reliability infrastructure**.

### AI Incident Reconstruction — Regulated Enterprises

Banks, insurers, and healthcare organizations face a core compliance problem: when an AI decision is challenged, they cannot explain the reasoning path, only the outcome.

AgentStateProtocol enables **Forensic Replay**:

- Roll back to any checkpoint in the decision chain
- Replay the exact reasoning tree that produced the outcome
- Simulate what alternative branches would have decided
- Produce a step-by-step audit trail for regulators

Relevant compliance frameworks: **EU AI Act**, **ISO 42001**, **OSFI B-10**, **HIPAA**, **SR 11-7**

Example decisions subject to audit: loan rejections, insurance claim denials, fraud alerts, medical triage recommendations.

---

### Autonomous Workflow Recovery — Enterprise Automation

Multi-agent pipelines fail mid-execution. One agent times out. A tool call crashes. Memory resets. Today, the entire workflow restarts from zero — losing all intermediate computation.

AgentStateProtocol enables **Stateful Recovery**:

```python
# Agent was processing step 14 of 20 when the API timed out.
# Without AgentStateProtocol: restart from step 1.
# With AgentStateProtocol: resume from step 13.

result, cp = agent.safe_execute(
    func=call_external_api,
    state=current_state,
    description="Fetch supplier data",
    max_retries=3,
    fallback=use_cached_supplier_data,
)
```

High-value industries: supply chain automation, claims processing, legal document generation, enterprise RAG pipelines.

---

### AI Governance Sandbox — Safe Experimentation

Enterprises are afraid to test new prompts or tools in production because failures cascade unpredictably.

AgentStateProtocol provides **Version Control for Decision Intelligence**:

```python
# Baseline path
agent.checkpoint(state=baseline_state, description="Production behavior")

# Experiment on a branch — production is untouched
agent.branch("new-prompt-strategy")
agent.checkpoint(state=experimental_state, description="Experimental prompt")

# Compare
print(agent.diff("baseline-checkpoint-id", "experimental-checkpoint-id"))

# Promote the better outcome
agent.merge("new-prompt-strategy", strategy="prefer_higher_confidence")
```

---

### High-Stakes Multi-Step Planning — Defense, Finance, Infrastructure

In 30-step reasoning chains, a timeout at step 22 destroys the entire context. Restarting loses the accumulated understanding that makes the plan coherent.

AgentStateProtocol enables **Long-Horizon Cognition**:

- Partial rollback to the last coherent state
- Branch simulation of alternative strategies
- Resume long planning sessions after interruption

Applicable domains: strategic planning agents, financial modeling, infrastructure optimization, scenario simulation.

---

### AI-Assisted Legal Defense and Accountability

Wrongful automated decisions — credit denials, benefit rejections, algorithmic penalties — need to be challengeable. Today they are not, because there is no replayable record.

AgentStateProtocol creates a **challengeable reasoning record**:

- Stores checkpoints that can be replayed under cross-examination
- Enables lawyers and regulators to test alternative logical paths
- Provides a structured audit trail that satisfies due process requirements

---

### Developer Debugging — AI IDE with State History

Developers cannot see where their agents fail. Stack traces show exceptions, not the reasoning path that led to them.

AgentStateProtocol provides **Reasoning Visibility**:

```
+-- ? Task accepted [de3eec5f]
    +-- ? Plan generated [3a7996fa]
        +-- ? API failed [372aabc7]   <- failure entered here
        +-- ? Cache fallback [a4d4e95e]
        +-- ? Retry succeeded [330a3284]
            +-- ? Summary complete [67f8369a]
```

---

## Quick Start

```bash
pip install agentstateprotocol
```

```python
from agentstateprotocol import AgentStateProtocol

agent = AgentStateProtocol("research-agent")

agent.checkpoint(
    state={"task": "Find best coffee shops in NYC", "stage": "parse"},
    metadata={"confidence": 0.92},
    description="Parsed request",
    logic_step="parse_input",
)

agent.checkpoint(
    state={"task": "Find best coffee shops in NYC", "stage": "search", "results": ["Devocion", "La Cabra"]},
    metadata={"confidence": 0.87},
    description="Collected candidates",
    logic_step="search",
)

# Recover if next step fails
agent.rollback()

# Try a different path
agent.branch("reviews-first")
agent.checkpoint(
    state={"task": "Find best coffee shops in NYC", "stage": "reviews"},
    logic_step="review_aggregation",
)
```

---

## Core Features

### 1. Checkpointing

```python
cp = agent.checkpoint(
    state={"reasoning": "User likely prefers quiet places with Wi-Fi"},
    metadata={"confidence": 0.88, "tokens_used": 132},
    description="Preference inference",
    logic_step="infer_preferences",
)

print(cp.id, cp.hash)
```

### 2. Rollback

```python
agent.rollback()                              # One step back
agent.rollback(steps=3)                       # N steps back
agent.rollback(to_checkpoint_id="abc123")     # Jump to specific checkpoint
```

### 3. Branching

```python
agent.checkpoint(state={"strategy": "stepwise"})
agent.branch("creative")
agent.checkpoint(state={"strategy": "lateral"})
agent.switch_branch("main")
```

### 4. Safe Execution with Recovery

```python
def risky_api_call(state):
    return call_external_api(state["query"])

result, cp = agent.safe_execute(
    func=risky_api_call,
    state={"query": "latest market headlines"},
    description="fetch_headlines",
    max_retries=3,
    fallback=use_cached_data,
)
```

### 5. Logic Tree Visualization

```python
print(agent.visualize_tree())
```

### 6. Decorator Integration

```python
from agentstateprotocol.decorators import agentstateprotocol_step

@agentstateprotocol_step("analyze_data")
def analyze(state):
    return {"analysis": process(state["data"])}

result = analyze({"data": raw_data})
```

---

## Recovery Strategies

| Strategy | Best For | Behavior |
|---|---|---|
| `RetryWithBackoff` | Timeouts / transient errors | Exponential retry delays |
| `AlternativePathStrategy` | Logical dead-ends | Shift to alternate path |
| `DegradeGracefully` | Resource pressure | Return reduced-complexity output |
| `CompositeStrategy` | Complex failure modes | Chain multiple strategies |

```python
from agentstateprotocol import AgentStateProtocol
from agentstateprotocol.strategies import RetryWithBackoff, DegradeGracefully, CompositeStrategy

agent = AgentStateProtocol(
    "resilient-agent",
    recovery_strategies=[
        CompositeStrategy([
            RetryWithBackoff(base_delay=1.0, max_delay=30.0),
            DegradeGracefully(),
        ]),
    ],
)
```

---

## Storage Backends

```python
from agentstateprotocol.storage import FileSystemStorage, SQLiteStorage

# File-based storage (easy to inspect)
agent = AgentStateProtocol("my-agent", storage_backend=FileSystemStorage(".agentstateprotocol"))

# SQLite storage (good for production querying)
agent = AgentStateProtocol("my-agent", storage_backend=SQLiteStorage("agent.db"))
```

| Backend | Best For | Persistence |
|---|---|---|
| `FileSystemStorage` | Development, debugging | JSON files on disk |
| `SQLiteStorage` | Production, audit logging | Single `.db` file |
| `InMemoryStorage` | Testing, ephemeral sessions | RAM only |

---

## CLI

```bash
agentstateprotocol demo
agentstateprotocol log
agentstateprotocol tree
agentstateprotocol branches
agentstateprotocol diff abc123 def456
agentstateprotocol inspect <id>
agentstateprotocol metrics
```

---

## Framework Integration

### LangChain-style Wrapping

```python
from agentstateprotocol.decorators import AgentStateProtocolMiddleware

middleware = AgentStateProtocolMiddleware("langchain-agent")
wrapped_chain = middleware.wrap(my_chain.invoke, "process_query")
result = wrapped_chain({"input": "Hello"})
```

### Generic Context Manager

```python
from agentstateprotocol.decorators import checkpoint_context

with checkpoint_context(description="Data processing") as ctx:
    result = process_data(data)
    ctx.state = {"result": result}
```

---

## Architecture

```
+-------------------------------------------------------------+
|                        Your AI Agent                        |
+-------------------------------------------------------------+
|  Decorators & Middleware (agentstateprotocol.decorators)    |
+-------------------------------------------------------------+
|     Core Engine (agentstateprotocol.engine)                 |
|   Checkpoint | Branch | Rollback | Logic Tree               |
+-------------------------------------------------------------+
|  Recovery Strategies (agentstateprotocol.strategies)        |
+-------------------------------------------------------------+
|  Serializers (agentstateprotocol.serializers)               |
+-------------------------------------------------------------+
|  Storage: FileSystem | SQLite | Memory                      |
+-------------------------------------------------------------+
```

---

## Compliance Alignment

AgentStateProtocol is designed with regulated AI deployment in mind:

| Requirement | How AgentStateProtocol Addresses It |
|---|---|
| **EU AI Act — Article 12** (Record-keeping) | Immutable checkpoint log with content hashes |
| **EU AI Act — Article 13** (Transparency) | Full reasoning tree replay and visualization |
| **ISO 42001** (AI Management System) | Auditable decision trail per agent session |
| **OSFI B-10** (Model Risk) | Branch comparison and outcome documentation |
| **SR 11-7** (Model Validation) | Replayable reasoning for model governance review |

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License — see [LICENSE](LICENSE).
