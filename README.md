# AgentStateProtocol

Checkpointing and recovery protocol for AI agents.

`AgentStateProtocol` lets an agent save state at each reasoning step, branch into alternatives, and roll back safely after failures.

## Install

```bash
pip install agentstateprotocol
```

## Quick Start

```python
from agentstateprotocol import AgentStateProtocol

agent = AgentStateProtocol("my-agent")

agent.checkpoint(
    state={"task": "summarize quarterly report", "stage": "parsed"},
    metadata={"confidence": 0.91},
    description="Initial parse",
    logic_step="parse_input",
)

agent.checkpoint(
    state={"task": "summarize quarterly report", "stage": "drafted"},
    metadata={"confidence": 0.86},
    description="Draft generated",
    logic_step="draft_summary",
)

# Roll back one step if needed
agent.rollback()
```

## Core Operations

- `agent.checkpoint(...)`: save a state snapshot
- `agent.rollback(...)`: restore a previous checkpoint
- `agent.branch(name)`: start an alternate reasoning path
- `agent.switch_branch(name)`: move between branches
- `agent.merge(source_branch)`: merge branch outcomes
- `agent.history()`: inspect checkpoint timeline
- `agent.visualize_tree()`: show decision tree

## Decorators

```python
from agentstateprotocol.decorators import agentstateprotocol_step

@agentstateprotocol_step("analyze")
def analyze(state):
    return {"result": "ok", **state}
```

## Storage

```python
from agentstateprotocol.storage import FileSystemStorage, SQLiteStorage

file_storage = FileSystemStorage(".agentstateprotocol")
sqlite_storage = SQLiteStorage(".agentstateprotocol/agentstateprotocol.db")
```

## CLI

```bash
agentstateprotocol demo
agentstateprotocol log
agentstateprotocol tree
agentstateprotocol branches
agentstateprotocol diff <checkpoint_a> <checkpoint_b>
agentstateprotocol metrics
```

## Project

- Repository: https://github.com/ekessh/agentstateprotocol
- License: MIT
