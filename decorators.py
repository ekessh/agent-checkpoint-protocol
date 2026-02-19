"""
Decorators & Integrations for AgentGit
========================================

Easy-to-use wrappers that let you add checkpointing to ANY agent
with minimal code changes.

Instead of rewriting your agent, just add a decorator:

    @agentgit_step("analyze_data")
    def analyze(state):
        # Your existing code here
        return result
"""

import functools
import time
import logging
from typing import Any, Callable, Dict, Optional

from .engine import AgentGit

logger = logging.getLogger("agentgit.decorators")

# Global agent registry (for decorator access)
_agent_registry: Dict[str, AgentGit] = {}


def get_agent(name: str = "default") -> AgentGit:
    """Get or create a named AgentGit instance."""
    if name not in _agent_registry:
        _agent_registry[name] = AgentGit(name)
    return _agent_registry[name]


def register_agent(name: str, agent: AgentGit) -> None:
    """Register an AgentGit instance for use with decorators."""
    _agent_registry[name] = agent


def agentgit_step(
    step_name: str,
    agent_name: str = "default",
    auto_rollback: bool = True,
    max_retries: int = 1,
):
    """
    Decorator that wraps a function with automatic checkpointing.
    
    Usage:
        @agentgit_step("parse_input")
        def parse_user_input(state):
            # parse logic here
            return updated_state
    
    What it does:
    1. Before the function runs: saves a checkpoint
    2. Runs the function
    3. After success: saves another checkpoint with the result
    4. On failure: rolls back to the pre-execution checkpoint
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            agent = get_agent(agent_name)
            
            # Determine state from first argument or kwargs
            state = {}
            if args and isinstance(args[0], dict):
                state = args[0]
            elif "state" in kwargs:
                state = kwargs["state"]
            
            # Checkpoint before execution
            pre_cp = agent.checkpoint(
                state=state,
                metadata={"step": step_name, "phase": "pre_execution"},
                description=f"Before: {step_name}",
                logic_step=step_name,
            )
            
            # Execute with retry
            last_error = None
            for attempt in range(max_retries):
                try:
                    start = time.time()
                    result = func(*args, **kwargs)
                    elapsed = time.time() - start
                    
                    # Checkpoint after success
                    result_state = result if isinstance(result, dict) else {"result": result}
                    agent.checkpoint(
                        state=result_state,
                        metadata={
                            "step": step_name,
                            "phase": "post_execution",
                            "duration_ms": round(elapsed * 1000, 2),
                            "attempt": attempt + 1,
                        },
                        description=f"After: {step_name}",
                        logic_step=f"{step_name}:done",
                    )
                    return result
                    
                except Exception as e:
                    last_error = e
                    logger.warning(f"Step '{step_name}' failed (attempt {attempt + 1}): {e}")
                    if auto_rollback:
                        agent.rollback(to_checkpoint_id=pre_cp.id)
            
            raise last_error
        
        return wrapper
    return decorator


def checkpoint_context(
    agent_name: str = "default",
    description: str = "",
):
    """
    Context manager for checkpointing a block of code.
    
    Usage:
        with checkpoint_context(description="Data processing") as ctx:
            result = process_data(data)
            ctx.state = {"result": result}
    
    On exception, automatically rolls back.
    """
    class CheckpointContext:
        def __init__(self):
            self.agent = get_agent(agent_name)
            self.state = {}
            self._pre_cp = None
        
        def __enter__(self):
            self._pre_cp = self.agent.checkpoint(
                state={},
                description=f"Context start: {description}",
                logic_step=description,
            )
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                # Error occurred — roll back
                logger.warning(f"Context '{description}' failed: {exc_val}")
                self.agent.rollback(to_checkpoint_id=self._pre_cp.id)
                return False  # Re-raise the exception
            
            # Success — save final state
            if self.state:
                self.agent.checkpoint(
                    state=self.state,
                    description=f"Context complete: {description}",
                    logic_step=f"{description}:done",
                )
            return False
    
    return CheckpointContext()


class AgentGitMiddleware:
    """
    Middleware for agent frameworks (LangChain, CrewAI, AutoGen, etc.)
    
    Wraps any callable agent step with automatic checkpointing.
    
    Usage:
        middleware = AgentGitMiddleware("my-agent")
        
        # Wrap a LangChain chain
        result = middleware.wrap(my_chain.invoke)({"input": "hello"})
    """
    
    def __init__(self, agent_name: str, **kwargs):
        self.agent = AgentGit(agent_name, **kwargs)
        register_agent(agent_name, self.agent)
    
    def wrap(self, func: Callable, step_name: str = "") -> Callable:
        """Wrap a function with checkpointing."""
        name = step_name or getattr(func, "__name__", "unnamed_step")
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            state = {}
            if args and isinstance(args[0], dict):
                state = args[0]
            
            result, cp = self.agent.safe_execute(
                func=lambda s: func(*args, **kwargs),
                state=state,
                description=name,
            )
            return result
        
        return wrapper
    
    def get_history(self) -> list:
        return self.agent.history()
    
    def get_tree(self) -> str:
        return self.agent.visualize_tree()
