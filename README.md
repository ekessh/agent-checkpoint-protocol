# AgentGit — Decision State Infrastructure for Regulated AI

**An open-source Checkpointing & Recovery Protocol for AI Agents**

> Capture, replay, and audit every step of an AI agent's reasoning chain. When a model hits a failure, it recovers to the last valid state and continues — without starting over. When a decision is challenged, you can replay exactly how it was reached.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-41%20passed-brightgreen.svg)]()

---

## The Problem

Modern AI agents make high-stakes decisions — loan approvals, claim denials, triage suggestions, fraud alerts — but leave behind no replayable record of how they got there. When something goes wrong:

- Logs show **inputs and outputs**, not the reasoning path
- Multi-step failures force a **full restart**, losing all intermediate state
- There is **no forensic trail** for compliance, audit, or legal challenge
- Developers **can't see where hallucination entered** the chain

This isn't a developer experience problem. It's a **reliability and governance gap** that blocks enterprise adoption of agentic AI.

## The Solution

AgentGit is a **checkpointing and recovery substrate** for AI agents. Every reasoning step is saved as a versioned state snapshot. Failures trigger automatic recovery. Every decision path is replayable.

| Git Concept | AgentGit Equivalent | What It Means |
|---|---|---|
| `git commit` | `agent.checkpoint()` | Save the agent's current reasoning state |
| `git reset` | `agent.rollback()` | Undo failed reasoning, restore last valid state |
| `git branch` | `agent.branch()` | Explore alternative decision paths in parallel |
| `git merge` | `agent.merge()` | Select and combine the best reasoning path |
| `git log` | `agent.history()` | Full audit trail of every decision step |
| `git diff` | `agent.diff()` | Compare what changed between two reasoning states |

---

## Why This Matters: Mission-Critical Use Cases

Checkpointing is not a convenience feature. In the following domains, it is **reliability infrastructure**.

### AI Incident Reconstruction — Regulated Enterprises

Banks, insurers, and healthcare organizations face a core compliance problem: when an AI decision is challenged, they cannot explain the reasoning path, only the outcome.

AgentGit enables **Forensic Replay**:

- Roll back to any checkpoint in the decision chain
- Replay the exact reasoning tree that produced the outcome
- Simulate what alternative branches would have decided
- Produce a step-by-step audit trail for regulators

Relevant compliance frameworks: **EU AI Act**, **ISO 42001**, **OSFI B-10**, **HIPAA**, **SR 11-7**

Example decisions subject to audit: loan rejections, insurance claim denials, fraud alerts, medical triage recommendations.

---

### Autonomous Workflow Recovery — Enterprise Automation

Multi-agent pipelines fail mid-execution. One agent times out. A tool call crashes. Memory resets. Today, the entire workflow restarts from zero — losing all intermediate computation.

AgentGit enables **Stateful Recovery**:

```python
# Agent was processing step 14 of 20 when the API timed out.
# Without AgentGit: restart from step 1.
# With AgentGit: resume from step 13.

result, cp = agent.safe_execute(
    func=call_external_api,
    state=current_state,
    description="Fetch supplier data",
    max_retries=3,
    fallback=use_cached_supplier_data
)
```

High-value industries: supply chain automation, claims processing, legal document generation, enterprise RAG pipelines.

---

### AI Governance Sandbox — Safe Experimentation

Enterprises are afraid to test new prompts or tools in production because failures cascade unpredictably.

AgentGit provides **Version Control for Decision Intelligence**:

- Save the current reasoning path before any experiment
- Branch to test a new prompt or tool strategy
- Compare outcome trees across branches
- Merge the winning path back into production

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

AgentGit enables **Long-Horizon Cognition**:

- Partial rollback to the last coherent state
- Branch simulation of alternative strategies
- Resume long planning sessions after interruption

Applicable domains: strategic planning agents, financial modeling, infrastructure optimization, scenario simulation.

---

### AI-Assisted Legal Defense and Accountability

Wrongful automated decisions — credit denials, benefit rejections, algorithmic penalties — need to be challengeable. Today they are not, because there is no replayable record.

AgentGit creates a **challengeable reasoning record**:

- Stores checkpoints that can be replayed under cross-examination
- Enables lawyers and regulators to test alternative logical paths
- Provides a structured audit trail that satisfies due process requirements

---

### Developer Debugging — AI IDE with State History

Developers cannot see where their agents fail. Stack traces show exceptions, not the reasoning path that led to them.

AgentGit provides **Reasoning Visibility**:

```bash
# Visualize the full decision tree
agentgit tree

# Find exactly where the logic broke
agentgit inspect <checkpoint-id>

# Compare the last two decision states
agentgit diff HEAD~1 HEAD
```

```
└── ✅ Task received [de3eec5f]
    └── ✅ Plan created [3a7996fa]
        ├── ❌ API call failed [372aabc7]   ← failure entered here
        ├── ✅ Used cache instead [a4d4e95e]
        └── ✅ Retry succeeded [330a3284]
            └── ✅ Summary generated [67f8369a]
```

---

## Quick Start

```bash
pip install agentgit
```

```python
from agentgit import AgentGit

agent = AgentGit("loan-decision-agent")

# Step 1: Capture state at each reasoning step
agent.checkpoint(
    state={"applicant_id": "A-4821", "income_verified": True, "dti_ratio": 0.38},
    metadata={"confidence": 0.91, "model": "gpt-4o"},
    description="Income and DTI verification complete",
    logic_step="verify_financials"
)

# Step 2: Continue reasoning
agent.checkpoint(
    state={"credit_score": 710, "risk_band": "medium", "flag": None},
    metadata={"confidence": 0.87},
    description="Credit assessment complete",
    logic_step="assess_credit"
)

# Step 3: API call to fraud service fails
# Roll back to last valid state — no restart required
agent.rollback()

# Or branch to try an alternative fraud detection approach
agent.branch("fallback-fraud-check")
agent.checkpoint(
    state={"fraud_check": "rule_based_fallback", "score": 0.12},
    description="Fallback fraud check applied",
    logic_step="fraud_detection_fallback"
)
```

---

## Core Features

### Checkpointing — Immutable State Snapshots

```python
cp = agent.checkpoint(
    state={"reasoning": "Applicant qualifies under Tier 2 criteria..."},
    metadata={"confidence": 0.87, "tokens_used": 150, "model": "gpt-4o"},
    description="Qualification decision",
    logic_step="qualification_check"
)
# Every checkpoint has a unique ID and content hash for integrity verification
print(f"Checkpoint: {cp.id} | Hash: {cp.hash} | Time: {cp.human_time}")
```

### Rollback — Restore to Any Prior State

```python
agent.rollback()                              # One step back
agent.rollback(steps=3)                       # Three steps back
agent.rollback(to_checkpoint_id="abc123")     # Jump to specific checkpoint
```

### Branching — Parallel Decision Paths

```python
agent.checkpoint(state={"approach": "conservative-underwriting"})

agent.branch("aggressive-underwriting")
agent.checkpoint(state={"approach": "higher-risk-tolerance"})

# Compare outcomes, then merge the better branch
agent.switch_branch("main")
agent.merge("aggressive-underwriting", strategy="prefer_higher_confidence")
```

### Safe Execution — Automatic Recovery

```python
def call_fraud_api(state):
    return fraud_service.check(state["applicant_id"])

result, checkpoint = agent.safe_execute(
    func=call_fraud_api,
    state=current_state,
    description="Fraud score lookup",
    max_retries=3,
    fallback=rule_based_fraud_check
)
```

### Logic Tree — Full Decision Audit Trail

```python
print(agent.visualize_tree())
# Produces a replayable decision tree from first checkpoint to current state
```

### Decorators — Zero-Code-Change Integration

```python
from agentgit.decorators import agentgit_step

@agentgit_step("classify_intent")
def classify(state):
    # Existing code, unchanged. Automatically checkpointed.
    return {"intent": model.classify(state["input"])}
```

---

## Recovery Strategies

| Strategy | When to Use | Behavior |
|---|---|---|
| `RetryWithBackoff` | API timeouts, rate limits | Exponential backoff between retries |
| `AlternativePathStrategy` | Logic dead-ends, tool failures | Switches to a registered alternative function |
| `DegradeGracefully` | Resource constraints | Reduces output complexity to stay functional |
| `CompositeStrategy` | Complex failure modes | Chains strategies — tries each in order |

```python
from agentgit.strategies import RetryWithBackoff, DegradeGracefully, CompositeStrategy

agent = AgentGit(
    "resilient-agent",
    recovery_strategies=[
        CompositeStrategy([
            RetryWithBackoff(base_delay=1.0, max_delay=30.0),
            DegradeGracefully(),
        ])
    ]
)
```

---

## Storage Backends

```python
from agentgit.storage import FileSystemStorage, SQLiteStorage

# File-based — human-readable JSON, ideal for development and debugging
agent = AgentGit("my-agent", storage_backend=FileSystemStorage(".agentgit"))

# SQLite — fast queries, filterable by branch, suitable for production
agent = AgentGit("my-agent", storage_backend=SQLiteStorage("agent.db"))
```

| Backend | Best For | Persistence |
|---|---|---|
| `FileSystemStorage` | Development, debugging | JSON files on disk |
| `SQLiteStorage` | Production, audit logging | Single `.db` file |
| `InMemoryStorage` | Testing, ephemeral sessions | RAM only |

---

## CLI

```bash
agentgit demo                     # Interactive walkthrough
agentgit log                      # Full checkpoint history
agentgit tree                     # Visualize reasoning tree
agentgit branches                 # List all decision branches
agentgit diff <id1> <id2>         # Compare two reasoning states
agentgit inspect <id>             # Detailed checkpoint view
agentgit metrics                  # Agent reliability statistics
```

---

## Framework Integration

### LangChain
```python
from agentgit.decorators import AgentGitMiddleware

middleware = AgentGitMiddleware("langchain-agent")
wrapped_chain = middleware.wrap(my_chain.invoke, "process_query")
result = wrapped_chain({"input": "Evaluate this loan application"})
```

### Any Python Agent
```python
from agentgit.decorators import checkpoint_context

with checkpoint_context(description="Document analysis") as ctx:
    result = analyze_document(doc)
    ctx.state = {"result": result, "page_count": len(doc.pages)}
# Automatically rolls back on exception
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Your AI Agent                     │
├─────────────────────────────────────────────────────┤
│     Decorators & Middleware  (agentgit.decorators)   │
├─────────────────────────────────────────────────────┤
│          AgentGit Core Engine  (agentgit.engine)     │
│   ┌──────────┐ ┌────────┐ ┌──────────┐ ┌─────────┐  │
│   │Checkpoint│ │ Branch │ │ Rollback │ │LogicTree│  │
│   └──────────┘ └────────┘ └──────────┘ └─────────┘  │
├─────────────────────────────────────────────────────┤
│       Recovery Strategies  (agentgit.strategies)     │
├─────────────────────────────────────────────────────┤
│           Serializers  (agentgit.serializers)        │
├─────────────────────────────────────────────────────┤
│    Storage:  FileSystem  │  SQLite  │  In-Memory     │
└─────────────────────────────────────────────────────┘
```

---

## Compliance Alignment

AgentGit is designed with regulated AI deployment in mind:

| Requirement | How AgentGit Addresses It |
|---|---|
| **EU AI Act — Article 12** (Record-keeping) | Immutable checkpoint log with content hashes |
| **EU AI Act — Article 13** (Transparency) | Full reasoning tree replay and visualization |
| **ISO 42001** (AI Management System) | Auditable decision trail per agent session |
| **OSFI B-10** (Model Risk) | Branch comparison and outcome documentation |
| **SR 11-7** (Model Validation) | Replayable reasoning for model governance review |

---

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, coding standards, and the PR checklist.

## License

MIT License — see [LICENSE](LICENSE) for details.
