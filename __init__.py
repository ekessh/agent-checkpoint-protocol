"""
AgentGit — Git for AI Thoughts
================================
An open-source Checkpointing & Recovery Protocol for AI Agents.

Save, branch, rollback, and recover agent "state of mind" at every reasoning step.
Think of it as version control for AI cognition.

Quick Start:
    from agentgit import AgentGit

    agent = AgentGit("my-agent")
    
    agent.checkpoint(
        state={"reasoning": "Analyzing user query..."},
        metadata={"step": "initial_analysis"}
    )
    
    # If something goes wrong, rollback:
    agent.rollback()
    
    # Or branch to explore alternative reasoning:
    agent.branch("alternative-approach")

License: MIT
"""

__version__ = "0.1.0"
__author__ = "AgentGit Contributors"

from .engine import AgentGit, Checkpoint, Branch, LogicTree
from .strategies import RecoveryStrategy, RetryWithBackoff, AlternativePathStrategy
from .serializers import StateSerializer, JSONSerializer, PickleSerializer
from .storage import StorageBackend, FileSystemStorage, SQLiteStorage

__all__ = [
    "AgentGit",
    "Checkpoint",
    "Branch",
    "LogicTree",
    "RecoveryStrategy",
    "RetryWithBackoff",
    "AlternativePathStrategy",
    "StateSerializer",
    "JSONSerializer",
    "PickleSerializer",
    "StorageBackend",
    "FileSystemStorage",
    "SQLiteStorage",
]
