# 🚀 Getting Started with SmartLLM Router

## Installation

```bash
pip install -e .
```

## Quick Start

1. Set your API keys:
```python
from smartllm_router import SmartRouter

router = SmartRouter(
    openai_key="your-openai-key",
    strategy="cost_optimized"
)
```

2. Use it like OpenAI:
```python
response = router.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Running Tests

```bash
pytest tests/
```

## Examples

See the `examples/` directory for more usage examples.
