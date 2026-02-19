# 🧠 AgentGit — Git for AI Thoughts

**An open-source Checkpointing & Recovery Protocol for AI Agents**

> Save, branch, rollback, and recover an agent's "state of mind" at every reasoning step. If the model hits a bug or a timeout, it rolls back to the last logical state and tries a different path — without starting over.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-41%20passed-brightgreen.svg)]()

---

## The Problem

AI agents are **fragile**. When a multi-step reasoning chain fails at step 7, most frameworks throw everything away and start from scratch. That's like closing your entire Word document because you made a typo on page 3.

## The Solution

AgentGit gives your agent a **version-controlled brain**:

| Git Concept | AgentGit Equivalent | What It Means |
|---|---|---|
| `git commit` | `agent.checkpoint()` | Save the agent's current "thought" |
| `git reset` | `agent.rollback()` | Undo bad reasoning, go back to a good state |
| `git branch` | `agent.branch()` | Explore alternative solutions in parallel |
| `git merge` | `agent.merge()` | Combine the best ideas from different paths |
| `git log` | `agent.history()` | View the full reasoning timeline |
| `git diff` | `agent.diff()` | See what changed between two thought-states |

---

## Quick Start

```bash
pip install agentgit
```

```python
from agentgit import AgentGit

# Initialize — like 'git init' for your agent's brain
agent = AgentGit("my-research-agent")

# Step 1: Save the agent's initial understanding
agent.checkpoint(
    state={"task": "Find best restaurants in NYC", "status": "parsing"},
    metadata={"confidence": 0.9},
    description="Parsed user request",
    logic_step="parse_input"
)

# Step 2: Agent does some work...
agent.checkpoint(
    state={"task": "Find best restaurants in NYC", "results": ["Le Bernardin", "Eleven Madison Park"]},
    metadata={"confidence": 0.85},
    description="Found top restaurants",
    logic_step="search_restaurants"
)

# Step 3: Oh no, the API timed out on the next step!
# No problem — just roll back.
agent.rollback()  # Goes back to "Found top restaurants"

# Or try a completely different approach
agent.branch("alternative-search")
agent.checkpoint(
    state={"task": "Find best restaurants in NYC", "approach": "Use cached reviews"},
    logic_step="cached_search"
)
```

---

## Core Features

### 1. Checkpointing — Save Points for the Brain

```python
cp = agent.checkpoint(
    state={"reasoning": "The user wants X because of Y..."},
    metadata={"confidence": 0.87, "tokens_used": 150},
    description="Identified user intent",
    logic_step="intent_classification"
)
# Every checkpoint gets a unique ID and content hash
print(f"Saved: {cp.id} (hash: {cp.hash})")
```

### 2. Rollback — Ctrl+Z for Thinking

```python
# Go back one step
agent.rollback()

# Go back 3 steps
agent.rollback(steps=3)

# Jump to a specific checkpoint
agent.rollback(to_checkpoint_id="abc123")
```

### 3. Branching — Explore Multiple Approaches

```python
# Main path: conservative approach
agent.checkpoint(state={"approach": "step-by-step"})

# Branch off to try something creative
agent.branch("creative")
agent.checkpoint(state={"approach": "lateral-thinking"})

# Go back to main if creative doesn't work
agent.switch_branch("main")
```

### 4. Safe Execution — Automatic Error Recovery

```python
def risky_api_call(state):
    # This might fail due to rate limits, timeouts, etc.
    return call_external_api(state["query"])

result, checkpoint = agent.safe_execute(
    func=risky_api_call,
    state={"query": "latest news"},
    description="Fetch news articles",
    max_retries=3,
    fallback=use_cached_data  # Plan B if all retries fail
)
```

### 5. Logic Tree — Full Decision Audit Trail

```python
print(agent.visualize_tree())
```

Output:
```
└── ✅ Task received [de3eec5f]
    └── ✅ Plan created [3a7996fa]
        ├── ❌ API call failed [372aabc7]
        ├── ✅ Used cache instead [a4d4e95e]
        └── ✅ Retry succeeded [330a3284]
            └── ✅ Summary generated [67f8369a]
```

### 6. Decorators — Zero-Code-Change Integration

```python
from agentgit.decorators import agentgit_step

@agentgit_step("analyze_data")
def analyze(state):
    # Your existing code — unchanged!
    return {"analysis": process(state["data"])}

# Automatically checkpointed, with rollback on failure
result = analyze({"data": raw_data})
```

---

## Recovery Strategies

| Strategy | When to Use | What It Does |
|---|---|---|
| `RetryWithBackoff` | API timeouts, rate limits | Waits longer between each retry |
| `AlternativePathStrategy` | Logic dead-ends | Switches to a different approach |
| `DegradeGracefully` | Resource limits | Produces simpler output |
| `CompositeStrategy` | Complex scenarios | Chains multiple strategies |

```python
from agentgit import AgentGit
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

# File-based (great for debugging — you can read the JSON files)
agent = AgentGit("my-agent", storage_backend=FileSystemStorage(".agentgit"))

# SQLite (fast queries, good for production)
agent = AgentGit("my-agent", storage_backend=SQLiteStorage("agent.db"))
```

---

## CLI

```bash
# Run the interactive demo
agentgit demo

# View checkpoint history
agentgit log

# Visualize the reasoning tree
agentgit tree

# List branches
agentgit branches

# Compare two checkpoints
agentgit diff abc123 def456

# View metrics
agentgit metrics
```

---

## Framework Integration

### LangChain
```python
from agentgit.decorators import AgentGitMiddleware

middleware = AgentGitMiddleware("langchain-agent")
wrapped_chain = middleware.wrap(my_chain.invoke, "process_query")
result = wrapped_chain({"input": "Hello"})
```

### Any Python Agent
```python
from agentgit.decorators import checkpoint_context

with checkpoint_context(description="Data processing") as ctx:
    result = process_data(data)
    ctx.state = {"result": result}
# Auto-rolls back on exception
```

---

## Architecture

```
┌──────────────────────────────────────────────────┐
│                   Your AI Agent                   │
├──────────────────────────────────────────────────┤
│    Decorators & Middleware (agentgit.decorators)   │
├──────────────────────────────────────────────────┤
│         AgentGit Core Engine (agentgit.engine)    │
│  ┌─────────┐ ┌────────┐ ┌────────┐ ┌──────────┐ │
│  │Checkpoint│ │ Branch │ │Rollback│ │Logic Tree│ │
│  └─────────┘ └────────┘ └────────┘ └──────────┘ │
├──────────────────────────────────────────────────┤
│    Recovery Strategies (agentgit.strategies)      │
├──────────────────────────────────────────────────┤
│      Serializers (agentgit.serializers)           │
├──────────────────────────────────────────────────┤
│   Storage Backends: FileSystem │ SQLite │ Memory  │
└──────────────────────────────────────────────────┘
```

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
