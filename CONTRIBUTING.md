# Contributing to LLM COGS Optimizer

Thank you for your interest in contributing! We want to make this tool the standard for efficient LLM workflows.

## How to Contribute

1.  **Fork the repository** and create your branch from `main`.
2.  **Install dependencies**: `pip install -e ".[dev]"`
3.  **Run tests**: We use `pytest`. Run `pytest tests/` (add tests if you add features!).
4.  **Linting**: Ensure your code is formatted with `black`.

## Areas for Contribution

- **New Providers**: Add support for Anthropic, Azure OpenAI, Bedrock, etc.
- **Better Analyzers**: Implement model-based complexity classification (e.g., using a tiny BERT model).
- **Dashboard**: A simple web UI to visualize cost savings over time.
- **Async Streaming**: Support for streaming responses from providers.

## Pull Request Process

1.  Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2.  Update the README.md with details of changes to the interface.
3.  Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
