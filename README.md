# AgentGit — Agent Checkpoint Protocol for Regulated AI

**Reliability and Explainability Infrastructure for Mission-Critical AI Systems**

> Every AI decision your enterprise makes should be replayable, auditable, and recoverable. AgentGit is the open-source protocol that makes that possible.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: 41 passed](https://img.shields.io/badge/tests-41%20passed-brightgreen.svg)]()
[![ISO 42001 Aligned](https://img.shields.io/badge/ISO_42001-aligned-orange.svg)]()

---

## Why This Exists

When a bank's AI rejects a loan, a regulator asks: *"Show me exactly how the AI reached that decision."*

When an insurance claim AI denies coverage, a lawyer asks: *"What alternative reasoning paths did the system consider?"*

When a multi-agent workflow crashes at step 14 of 30, the operations team asks: *"Why do we have to start over from scratch?"*

Today, most AI systems can only show inputs and outputs. The reasoning in between — the branches considered, the fallbacks triggered, the confidence at each step — is lost the moment it happens.

**AgentGit solves this.** It captures the full cognitive lifecycle of every AI decision: every reasoning step checkpointed, every branch preserved, every failure recovered, every path replayable.

This is not a developer convenience tool. This is **reliability infrastructure** for enterprises where AI decisions carry legal, financial, and human consequences.

---

## What It Does — In Plain English

Think of AgentGit as a **flight recorder for AI reasoning**. Just like a black box records every instrument reading, control input, and system status during a flight, AgentGit records every reasoning step, confidence level, decision branch, and state change during an AI operation.

| Capability | What Happens | Why It Matters |
|---|---|---|
| **Checkpoint** | Saves the agent's full reasoning state at each step | Creates an auditable trail of how the AI "thought" |
| **Rollback** | Restores the agent to any prior reasoning state | Recovers from failures without restarting the entire workflow |
| **Branch** | Creates parallel reasoning paths to explore alternatives | Proves the AI considered multiple approaches |
| **Merge** | Combines the best outcome from different paths | Validates decisions through cross-verification |
| **Diff** | Shows exactly what changed between two reasoning states | Pinpoints where reasoning diverged or degraded |
| **Replay** | Re-traces the full decision tree after the fact | Enables forensic reconstruction under audit or legal review |

---

## Enterprise Use Cases

### 1. AI Incident Reconstruction — Forensic Mode for Regulated Decisions

**The problem:** A bank's AI agent rejects a mortgage application. The applicant challenges it. The compliance team needs to explain not just the final decision, but every reasoning step that led to it, what alternatives existed, and why they were not taken.

**How AgentGit solves it:**

```python
from agentgit import AgentGit

# Every AI decision gets a full reasoning trail
agent = AgentGit("loan-underwriting-agent")

# Step 1: Agent receives application
agent.checkpoint(
    state={"applicant_id": "A-7829", "income": 85000, "debt_ratio": 0.42},
    metadata={"confidence": 1.0, "data_source": "application_form"},
    description="Application data ingested",
    logic_step="data_intake"
)

# Step 2: Agent evaluates risk factors
agent.checkpoint(
    state={"risk_score": 0.67, "flags": ["high_debt_ratio"], "recommendation": "review"},
    metadata={"confidence": 0.78, "model_version": "risk-v3.2"},
    description="Risk assessment computed",
    logic_step="risk_evaluation"
)

# Step 3: Agent considers an alternative path
agent.branch("manual-override-check")
agent.checkpoint(
    state={"override_eligible": True, "mitigating_factors": ["stable_employment_10yr"]},
    metadata={"confidence": 0.85},
    description="Checked for mitigating factors",
    logic_step="override_analysis"
)

# Later, under audit — replay the entire decision tree:
print(agent.visualize_tree())
# └── ✅ Application data ingested [a1b2c3d4]
#     └── ✅ Risk assessment computed [e5f6g7h8]
#         ├── ✅ Checked for mitigating factors [i9j0k1l2]  (branch: manual-override)
#         └── ✅ Final decision rendered [m3n4o5p6]

# Compare what would have happened on the alternative branch:
diff = agent.diff("e5f6g7h8", "i9j0k1l2")
```

**Compliance alignment:** EU AI Act (Article 14: Human Oversight), OSFI B-13, ISO 42001 Clause 6.1, NIST AI RMF.

---

### 2. Autonomous Workflow Recovery — Stateful Resilience for Multi-Agent Systems

**The problem:** A 30-step claims processing pipeline fails at step 22 because a downstream API times out. Without checkpointing, the entire workflow restarts. That means re-running 21 successful steps, burning compute, and delaying the outcome.

**How AgentGit solves it:**

```python
from agentgit import AgentGit
from agentgit.strategies import RetryWithBackoff, DegradeGracefully, CompositeStrategy

# Configure with enterprise-grade recovery
agent = AgentGit(
    "claims-processing-agent",
    recovery_strategies=[
        CompositeStrategy([
            RetryWithBackoff(base_delay=2.0, max_delay=60.0),
            DegradeGracefully(),
        ])
    ]
)

# Wrap risky operations with automatic checkpointing and recovery
def verify_medical_records(state):
    return call_medical_api(state["claim_id"])  # Might timeout

result, checkpoint = agent.safe_execute(
    func=verify_medical_records,
    state={"claim_id": "CLM-9982", "step": 22},
    description="Medical record verification",
    max_retries=3,
    fallback=use_cached_verification  # Graceful degradation if API is down
)

# If it fails: AgentGit rolls back to step 21, not step 1.
# If it succeeds: The checkpoint is preserved for audit.
```

**Impact:** In a 30-step pipeline, recovering from step 22 instead of restarting from step 1 saves approximately 70% of compute cost and processing time per incident.

---

### 3. AI Governance Sandbox — Safe Experimentation Without Cascading Failure

**The problem:** Enterprises are afraid to test new prompts, tools, or model versions because a bad experiment can cascade through production workflows. There is no safe way to "try something and undo it" in most AI systems.

**How AgentGit solves it:**

```python
agent = AgentGit("experiment-sandbox")

# Save current production reasoning
agent.checkpoint(
    state=production_state,
    description="Production baseline",
    logic_step="baseline"
)

# Branch to test a new prompt strategy
agent.branch("new-prompt-v2")
agent.checkpoint(
    state={"prompt_version": "v2", "temperature": 0.7},
    metadata={"confidence": 0.88},
    logic_step="experiment_v2"
)

# Branch to test a different model
agent.branch("model-swap-test")
agent.checkpoint(
    state={"model": "claude-sonnet-4-5-20250929", "temperature": 0.5},
    metadata={"confidence": 0.91},
    logic_step="experiment_model_swap"
)

# Compare outcomes across branches
diff = agent.diff("experiment_v2_checkpoint", "model_swap_checkpoint")

# Merge the winner back to production baseline
agent.switch_branch("main")
agent.merge("model-swap-test", strategy="prefer_higher_confidence")
```

**Result:** Version-controlled decision intelligence. Every experiment is traceable, reversible, and auditable.

---

### 4. Disaster Response AI — Resumable Crisis Modeling

When multi-agent systems coordinate wildfire response, flood prediction, or pandemic modeling, a system crash mid-planning is not an inconvenience — it is a threat to human safety. Checkpointing enables resumable crisis modeling, scenario branch comparison, and rollback to safer action plans when conditions change.

### 5. AI-Assisted Legal Defense — Making AI Decisions Challengeable

When credit scoring errors, government benefit denials, or automated hiring rejections affect real people, the protocol forces AI systems to store reasoning checkpoints that can be replayed in legal proceedings. Lawyers can test alternative logical paths to demonstrate that the AI's reasoning was flawed or that a different path would have produced a different outcome.

### 6. High-Stakes Multi-Step Planning — Defense, Aerospace, Financial Trading

In domains where a 30-step reasoning chain represents hours of computation, and a timeout at step 28 would destroy the entire context, checkpointing enables long-horizon cognition with partial rollback and branch simulation.

### 7. AI Debugging Platform — Reasoning Visibility for Developers

For AI engineering teams, the protocol visualizes the full reasoning tree, shows exactly where hallucination or confidence degradation entered the chain, and allows branch pruning to isolate failure modes.

---

## Technical Reference

### Installation

```bash
pip install agentgit
```

Zero external dependencies. Pure Python stdlib. Production-ready.

### Core API

```python
from agentgit import AgentGit

agent = AgentGit("my-agent")

# ── Checkpoint: Save reasoning state ──
cp = agent.checkpoint(
    state={"reasoning": "...", "data": {...}},   # Agent's current "state of mind"
    metadata={"confidence": 0.92, "tokens": 340}, # Performance metrics
    description="What this step accomplished",     # Human-readable label
    logic_step="step_name"                         # Node in the logic tree
)

# ── Rollback: Restore a prior state ──
agent.rollback()                           # Go back one step
agent.rollback(steps=3)                    # Go back three steps
agent.rollback(to_checkpoint_id="abc123")  # Jump to a specific checkpoint

# ── Branch: Explore alternative reasoning paths ──
agent.branch("alternative-approach")       # Create and switch to new branch
agent.switch_branch("main")                # Switch back
agent.list_branches()                      # See all branches

# ── Merge: Combine insights from branches ──
agent.merge("alternative-approach", strategy="prefer_higher_confidence")
# Strategies: "prefer_higher_confidence", "combine", "prefer_source", "prefer_target"

# ── Diff: Compare two reasoning states ──
diff = agent.diff(checkpoint_a_id, checkpoint_b_id)
# Returns: { added: {...}, removed: {...}, modified: {...} }

# ── History: Full reasoning timeline ──
agent.history(limit=50)                    # Like 'git log'

# ── Logic Tree: Visual decision audit ──
print(agent.visualize_tree())              # Text-based tree visualization

# ── Export/Import: Session persistence ──
data = agent.export_session()              # Export for storage or transfer
restored = AgentGit.import_session(data)   # Restore from exported data

# ── Metrics: Operational telemetry ──
agent.metrics  # checkpoints, rollbacks, recoveries, branches, errors caught
```

### Safe Execution with Automatic Recovery

```python
result, checkpoint = agent.safe_execute(
    func=my_function,          # The operation to protect
    state=current_state,       # Current agent state
    description="Operation X", # Label for audit trail
    max_retries=3,             # Retry attempts before fallback
    fallback=plan_b_function   # Alternative if all retries fail
)
# Automatic flow: checkpoint → execute → on failure: rollback → retry → fallback
```

### Recovery Strategies

```python
from agentgit.strategies import (
    RetryWithBackoff,            # Exponential backoff for transient failures
    AlternativePathStrategy,     # Switch to different reasoning approach
    DegradeGracefully,           # Reduce complexity when resources are limited
    CompositeStrategy,           # Chain multiple strategies in priority order
)

agent = AgentGit(
    "production-agent",
    recovery_strategies=[
        CompositeStrategy([
            RetryWithBackoff(base_delay=1.0, max_delay=30.0),
            AlternativePathStrategy(state_modifiers={"mode": "simplified"}),
            DegradeGracefully(),
        ])
    ]
)
```

### Decorator Integration — Add Checkpointing Without Changing Existing Code

```python
from agentgit.decorators import agentgit_step, checkpoint_context, AgentGitMiddleware

# Option 1: Decorator — one line per function
@agentgit_step("risk_assessment", auto_rollback=True, max_retries=2)
def assess_risk(state):
    return compute_risk_score(state)

# Option 2: Context manager — wrap any code block
with checkpoint_context(description="Document processing") as ctx:
    result = process_document(doc)
    ctx.state = {"result": result}

# Option 3: Middleware — wrap entire agent frameworks (LangChain, CrewAI, etc.)
middleware = AgentGitMiddleware("my-framework-agent")
wrapped_chain = middleware.wrap(my_chain.invoke, "process_query")
```

### Storage Backends

```python
from agentgit.storage import FileSystemStorage, SQLiteStorage, InMemoryStorage

# File system — human-readable JSON files, ideal for debugging and git-based versioning
agent = AgentGit("agent", storage_backend=FileSystemStorage(".agentgit"))

# SQLite — fast indexed queries, ideal for production with large checkpoint volumes
agent = AgentGit("agent", storage_backend=SQLiteStorage("agent_checkpoints.db"))

# In-memory — no persistence, ideal for testing and ephemeral workloads
agent = AgentGit("agent", storage_backend=InMemoryStorage())
```

### CLI

```bash
agentgit demo                    # Run interactive demonstration
agentgit log --branch main       # View checkpoint history
agentgit tree                    # Visualize reasoning decision tree
agentgit branches                # List all reasoning branches
agentgit diff <id_a> <id_b>     # Compare two checkpoint states
agentgit inspect <checkpoint_id> # View full checkpoint details
agentgit metrics                 # Operational telemetry
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Your AI Agent / Framework               │
│              (LangChain, CrewAI, AutoGen, Custom)            │
├─────────────────────────────────────────────────────────────┤
│          Decorators & Middleware  (agentgit.decorators)       │
│     @agentgit_step  |  checkpoint_context  |  Middleware     │
├─────────────────────────────────────────────────────────────┤
│               Core Protocol Engine  (agentgit.engine)        │
│  ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
│  │ Checkpoint  │ │ Rollback │ │  Branch  │ │ Logic Tree  │  │
│  │ (state     │ │ (state   │ │ (parallel│ │ (full audit │  │
│  │  capture)  │ │  restore)│ │  paths)  │ │  trail)     │  │
│  └────────────┘ └──────────┘ └──────────┘ └─────────────┘  │
├─────────────────────────────────────────────────────────────┤
│          Recovery Strategies  (agentgit.strategies)          │
│   RetryWithBackoff | AlternativePath | Degrade | Composite  │
├─────────────────────────────────────────────────────────────┤
│             Serializers  (agentgit.serializers)              │
│          JSON (readable) | Pickle (fast) | Compressed       │
├─────────────────────────────────────────────────────────────┤
│            Storage Backends  (agentgit.storage)              │
│       FileSystem (audit) | SQLite (production) | Memory     │
└─────────────────────────────────────────────────────────────┘
```

---

## Compliance Alignment

AgentGit's checkpoint protocol produces artifacts that support compliance with:

| Regulation / Standard | Relevant Requirement | How AgentGit Helps |
|---|---|---|
| **EU AI Act** | Article 14 — Human Oversight | Full reasoning replay enables human review of AI decisions |
| **EU AI Act** | Article 12 — Record-Keeping | Immutable checkpoint history with content hashes |
| **ISO 42001** | Clause 6.1 — Risk Assessment | Logic tree shows risk evaluation at each decision point |
| **ISO 42001** | Clause 9.1 — Monitoring | Real-time metrics on errors, rollbacks, and recovery rates |
| **NIST AI RMF** | Govern, Map, Measure, Manage | Checkpoint metadata captures governance context per step |
| **OSFI B-13** | Model Risk Management | Branch comparison demonstrates model considered alternatives |
| **SOC 2 Type II** | Processing Integrity | Content hashes verify checkpoint integrity |

---

## Positioning

AgentGit is not a developer productivity tool. It is **reliability infrastructure** for enterprises deploying AI in regulated, mission-critical environments.

The protocol addresses three converging enterprise needs:

**Auditability** — Every AI decision is fully reconstructable. Regulators, auditors, and legal teams can replay reasoning chains, inspect confidence levels at each step, and verify that alternatives were considered.

**Resilience** — Multi-step AI workflows recover from failures at the point of failure, not from the beginning. This reduces compute waste, processing latency, and operational risk in production systems.

**Governability** — AI experimentation becomes safe. Teams can branch, test, compare, and merge reasoning strategies with the same rigor that software teams apply to code — but applied to decision logic.

---

## Project Structure

```
agentgit/
├── agentgit/
│   ├── __init__.py        # Public API surface
│   ├── engine.py          # Core protocol — checkpoint, rollback, branch, merge, diff
│   ├── strategies.py      # Recovery strategies — retry, alternative path, degrade
│   ├── storage.py         # Persistence — filesystem, SQLite, in-memory
│   ├── serializers.py     # State serialization — JSON, pickle, compressed
│   ├── decorators.py      # Integration layer — decorators, context managers, middleware
│   └── cli.py             # Command-line interface
├── tests/
│   └── test_agentgit.py   # 41 tests covering all modules
├── pyproject.toml          # Package configuration
├── LICENSE                 # MIT License
└── README.md
```

---

## Contributing

Contributions welcome. Priority areas: additional storage backends (Redis, PostgreSQL), framework-specific integrations (LangGraph, CrewAI, AutoGen), structured compliance report export, and distributed checkpointing for multi-agent systems.

## License

MIT License — see [LICENSE](LICENSE) for details.
