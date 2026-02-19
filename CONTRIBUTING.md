# Contributing to AgentGit

Thanks for your interest in contributing to AgentGit. This guide explains how to propose changes, run tests, and submit high-quality pull requests.

## Development Setup

1. Fork the repository and clone your fork.
2. Create and activate a virtual environment.
3. Install development dependencies:

```bash
pip install -e .[dev]
```

## Project Structure

- `engine.py`: core checkpointing and recovery logic
- `decorators.py`: decorators and middleware helpers
- `storage.py`: storage backend implementations
- `strategies.py`: recovery strategy implementations
- `serializers.py`: serialization utilities
- `cli.py`: command-line interface
- `test_agentgit.py`: automated tests

## Coding Guidelines

- Target Python 3.9+ compatibility.
- Prefer clear, small functions with explicit behavior.
- Keep public APIs documented with concise docstrings.
- Avoid introducing breaking changes without discussion.

## Testing

Run the test suite before opening a pull request:

```bash
pytest
```

When changing behavior, include or update tests that cover:

- happy paths
- edge cases
- regression scenarios

## Commit Guidelines

Use focused commits with descriptive messages.

Recommended format:

- `feat: add branch merge conflict resolver`
- `fix: handle checkpoint rollback on empty history`
- `docs: clarify storage backend configuration`

## Pull Request Guidelines

Before submitting a PR, ensure:

1. Your branch is up to date with `main`.
2. Tests pass locally.
3. New functionality includes tests.
4. Documentation is updated when behavior changes.

In your PR description, include:

- what changed
- why it changed
- how it was tested
- any known limitations

## Reporting Issues

When opening an issue, include:

- environment details (OS, Python version)
- steps to reproduce
- expected behavior
- actual behavior
- logs or tracebacks when available

## Security

If you discover a security issue, please do not post exploit details publicly. Open a private report through GitHub security reporting if available.

## License

By contributing, you agree that your contributions are licensed under the MIT License.
