# Contributing to AgentStateProtocol

Thanks for your interest in contributing to AgentStateProtocol.

## Development Setup

1. Fork and clone the repository.
2. Create and activate a virtual environment.
3. Install dev dependencies:

```bash
pip install -e .[dev]
```

## Project Structure

- `agentstateprotocol/engine.py`: core checkpointing and recovery logic
- `agentstateprotocol/decorators.py`: decorators and middleware helpers
- `agentstateprotocol/storage.py`: storage backend implementations
- `agentstateprotocol/strategies.py`: recovery strategy implementations
- `agentstateprotocol/serializers.py`: serialization utilities
- `agentstateprotocol/cli.py`: command-line interface
- `test_agentstateprotocol.py`: automated tests

## Coding Guidelines

- Target Python 3.9+ compatibility.
- Prefer clear, small functions with explicit behavior.
- Keep public APIs documented with concise docstrings.
- Avoid introducing breaking changes without discussion.

## Testing

```bash
pytest
```

When changing behavior, include or update tests that cover:

- happy paths
- edge cases
- regression scenarios

## Commit Guidelines

Use focused commits with descriptive messages:

- `feat: add branch merge conflict resolver`
- `fix: handle checkpoint rollback on empty history`
- `docs: clarify storage backend configuration`

## Pull Requests

Before opening a PR:

1. Ensure your branch is up to date with `main`.
2. Tests pass locally.
3. New functionality includes tests.
4. Documentation is updated when behavior changes.

In your PR description, include what changed, why it changed, how it was tested, and any known limitations.

## Reporting Issues

When opening an issue, include environment details (OS, Python version), steps to reproduce, expected behavior, actual behavior, and logs or tracebacks when available.

## Security

If you discover a security issue, please do not post exploit details publicly. Open a private report through GitHub security reporting.

## License

By contributing, you agree that your contributions are licensed under the MIT License.
