# LLM COGS Optimizer

A middleware tool designed to optimize the Cost of Goods Sold (COGS) for LLM-based applications. It intelligently routes queries between low-cost local models (e.g., Ollama, Llama.cpp) and high-performance cloud APIs (e.g., Vertex AI, OpenAI) based on query complexity and cost configurations.

> **Note**: This project is intentionally designed to be simple and lightweight, providing a clean foundation that is easy to audit, integrate, and extend.

## Features

- **Smart Routing**: Analyzes query complexity to decide between local vs. cloud execution.
- **Cost Tracking**: Real-time estimation of savings.
- **Pluggable Providers**: Easy-to-extend interfaces for different model providers.
- **Async Support**: Built for high-performance agentic workflows.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from llm_cogs_optimizer.core.router import ModelRouter
from llm_cogs_optimizer.providers import OllamaProvider, VertexAIProvider

# Initialize providers
local = OllamaProvider(base_url="http://localhost:11434", model="llama3")
cloud = VertexAIProvider(project_id="my-project", location="us-central1")

# Initialize router
router = ModelRouter(local_provider=local, cloud_provider=cloud)

# Route and generate
response = await router.generate("What is the capital of France?")
print(response)
```

## Contributing

We welcome contributors! Please see `CONTRIBUTING.md` for details.
