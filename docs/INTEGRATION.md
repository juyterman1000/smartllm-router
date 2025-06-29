# 🔧 SmartLLM Router Integration Guide

Complete guide for integrating SmartLLM Router into your existing applications.

## 🚀 Quick Start (5 minutes)

### 1. Installation
```bash
pip install smartllm-router
```

### 2. Basic Setup
```python
from smartllm_router import SmartRouter

# Initialize with your API keys
router = SmartRouter(
    openai_key="sk-...",
    anthropic_key="sk-ant-...",
    strategy="balanced"
)

# Use exactly like OpenAI client
response = router.chat.completions.create(
    model="auto",  # Router decides the best model
    messages=[{"role": "user", "content": "Hello, world!"}]
)

print(f"Response: {response.content}")
print(f"Model used: {response.model}")
print(f"Cost: ${response.cost:.4f}")
print(f"Saved: ${response.savings:.4f}")
```

### 3. Drop-in Replacement
```python
# Before: OpenAI client
import openai
client = openai.OpenAI(api_key="sk-...")
response = client.chat.completions.create(...)

# After: SmartLLM Router (same interface!)
from smartllm_router import SmartRouter
router = SmartRouter(openai_key="sk-...")
response = router.chat.completions.create(...)
```

---

## 🏗️ Framework Integrations

### LangChain Integration

```python
from langchain.llms.base import LLM
from smartllm_router import SmartRouter
from typing import Optional, List, Any

class SmartLLMRouter(LLM):
    """LangChain wrapper for SmartLLM Router"""
    
    router: SmartRouter
    
    def __init__(self, **kwargs):
        super().__init__()
        self.router = SmartRouter(**kwargs)
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.router.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content
    
    @property
    def _llm_type(self) -> str:
        return "smartllm_router"

# Usage
llm = SmartLLMRouter(
    openai_key="sk-...",
    strategy="cost_optimized"
)

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question: {question}"
)

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("What is the capital of France?")
```

### LlamaIndex Integration

```python
from llama_index.llms.custom import CustomLLM
from llama_index.core.llms import CompletionResponse, LLMMetadata
from smartllm_router import SmartRouter

class SmartLLMRouterLlamaIndex(CustomLLM):
    """LlamaIndex wrapper for SmartLLM Router"""
    
    def __init__(self, **kwargs):
        super().__init__()
        self.router = SmartRouter(**kwargs)
    
    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=4096,
            num_output=1024,
            model_name="smartllm_router"
        )
    
    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        response = self.router.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return CompletionResponse(
            text=response.content,
            additional_kwargs={
                "model_used": response.model,
                "cost": response.cost,
                "savings": response.savings
            }
        )

# Usage
llm = SmartLLMRouterLlamaIndex(
    openai_key="sk-...",
    strategy="balanced"
)

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents, llm=llm)
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from smartllm_router import SmartRouter
import os

app = FastAPI(title="SmartLLM Router API")

# Initialize router
router = SmartRouter(
    openai_key=os.getenv("OPENAI_KEY"),
    anthropic_key=os.getenv("ANTHROPIC_KEY"),
    strategy="balanced"
)

class ChatRequest(BaseModel):
    message: str
    strategy: str = "balanced"

class ChatResponse(BaseModel):
    response: str
    model_used: str
    cost: float
    savings: float

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = router.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": request.message}],
            strategy=request.strategy
        )
        
        return ChatResponse(
            response=response.content,
            model_used=response.model,
            cost=response.cost,
            savings=response.savings
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    return router.get_analytics(period_days=7)

# Run with: uvicorn main:app --reload
```

### Flask Integration

```python
from flask import Flask, request, jsonify
from smartllm_router import SmartRouter
import os

app = Flask(__name__)

# Initialize router
router = SmartRouter(
    openai_key=os.getenv("OPENAI_KEY"),
    anthropic_key=os.getenv("ANTHROPIC_KEY"),
    strategy="balanced"
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    
    try:
        response = router.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": data['message']}]
        )
        
        return jsonify({
            "response": response.content,
            "model_used": response.model,
            "cost": response.cost,
            "savings": response.savings
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analytics')
def analytics():
    return jsonify(router.get_analytics(period_days=7))

if __name__ == '__main__':
    app.run(debug=True)
```

---

## ⚙️ Advanced Configuration

### Custom Routing Rules

```python
from smartllm_router import SmartRouter, RoutingRule

router = SmartRouter(strategy="balanced")

# Always use GPT-4 for code generation
router.add_rule(RoutingRule(
    name="code_generation",
    condition=lambda q: q.task_type == "code",
    model="gpt-4",
    priority=100
))

# Use cheaper models for simple Q&A
router.add_rule(RoutingRule(
    name="simple_qa",
    condition=lambda q: q.complexity_score < 0.3,
    model="claude-3-haiku",
    priority=90
))

# Budget-based routing
router.add_rule(RoutingRule(
    name="budget_control",
    condition=lambda q: router.tracker.daily_cost > 100.0,
    model="mistral-7b",  # Cheapest option
    priority=200  # Highest priority
))
```

### Environment-Based Configuration

```python
import os
from smartllm_router import SmartRouter

# Production configuration
if os.getenv("ENVIRONMENT") == "production":
    router = SmartRouter(
        openai_key=os.getenv("OPENAI_KEY"),
        anthropic_key=os.getenv("ANTHROPIC_KEY"),
        google_key=os.getenv("GOOGLE_KEY"),
        mistral_key=os.getenv("MISTRAL_KEY"),
        strategy="balanced",
        daily_budget=500.0,
        cache_ttl=3600,
        enable_fallback=True
    )
else:
    # Development configuration
    router = SmartRouter(
        openai_key=os.getenv("OPENAI_KEY"),
        strategy="cost_optimized",
        daily_budget=50.0,
        cache_ttl=300,
        enable_fallback=False
    )
```

### Async Support

```python
import asyncio
from smartllm_router import SmartRouter

async def process_queries_async(queries):
    router = SmartRouter(openai_key="sk-...")
    
    async def process_single_query(query):
        # Note: Current version is sync, async support coming soon
        return router.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": query}]
        )
    
    # Process queries concurrently
    tasks = [process_single_query(q) for q in queries]
    results = await asyncio.gather(*tasks)
    
    return results

# Usage
queries = ["What is AI?", "Explain quantum computing", "Write a Python function"]
results = asyncio.run(process_queries_async(queries))
```

---

## 📊 Monitoring & Analytics

### Real-time Monitoring

```python
from smartllm_router import SmartRouter
import time

router = SmartRouter(openai_key="sk-...")

# Process some queries
for i in range(10):
    response = router.chat.completions.create(
        model="auto",
        messages=[{"role": "user", "content": f"Query {i}"}]
    )
    print(f"Query {i}: {response.model} - ${response.cost:.4f}")

# Get analytics
analytics = router.get_analytics(period_days=1)
print(f"Total requests: {analytics['total_requests']}")
print(f"Total cost: ${analytics['total_cost']:.4f}")
print(f"Total savings: ${analytics['total_savings']:.4f}")
print(f"Cost reduction: {analytics['cost_reduction_percentage']:.1f}%")
```

### Custom Metrics

```python
import logging
from smartllm_router import SmartRouter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoredRouter(SmartRouter):
    """Router with custom monitoring"""
    
    def create(self, *args, **kwargs):
        start_time = time.time()
        
        try:
            response = super().create(*args, **kwargs)
            
            # Log successful request
            logger.info(f"Request successful: {response.model} - ${response.cost:.4f}")
            
            # Custom metrics
            self.track_custom_metric("request_success", 1)
            self.track_custom_metric("total_cost", response.cost)
            
            return response
            
        except Exception as e:
            # Log failed request
            logger.error(f"Request failed: {str(e)}")
            self.track_custom_metric("request_failure", 1)
            raise
        
        finally:
            latency = time.time() - start_time
            self.track_custom_metric("request_latency", latency)
    
    def track_custom_metric(self, name, value):
        # Implement your metrics tracking here
        # e.g., send to Prometheus, DataDog, etc.
        pass
```

---

## 🔒 Security & Compliance

### API Key Management

```python
import os
from smartllm_router import SmartRouter

# Use environment variables (recommended)
router = SmartRouter(
    openai_key=os.getenv("OPENAI_KEY"),
    anthropic_key=os.getenv("ANTHROPIC_KEY")
)

# Or use a secrets management service
from your_secrets_manager import get_secret

router = SmartRouter(
    openai_key=get_secret("openai_api_key"),
    anthropic_key=get_secret("anthropic_api_key")
)
```

### Data Privacy

```python
from smartllm_router import SmartRouter

# Configure for GDPR compliance
router = SmartRouter(
    openai_key="sk-...",
    strategy="balanced",
    cache_ttl=0,  # Disable caching for sensitive data
    enable_logging=False  # Disable request logging
)

# Add data residency rules
router.add_rule(RoutingRule(
    name="eu_data_residency",
    condition=lambda q: q.user_region == "EU",
    model="claude-3-haiku",  # EU-compliant provider
    priority=100
))
```

---

## 🧪 Testing

### Unit Testing

```python
import unittest
from unittest.mock import patch
from smartllm_router import SmartRouter

class TestSmartRouter(unittest.TestCase):
    
    def setUp(self):
        self.router = SmartRouter(
            openai_key="test-key",
            strategy="balanced"
        )
    
    @patch('smartllm_router.router.SmartRouter._call_openai_api')
    def test_simple_query_routing(self, mock_api):
        mock_api.return_value = "Test response"
        
        response = self.router.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": "What is 2+2?"}]
        )
        
        self.assertEqual(response.content, "Test response")
        self.assertGreater(response.savings, 0)
    
    def test_custom_rule_application(self):
        from smartllm_router import RoutingRule
        
        rule = RoutingRule(
            name="test_rule",
            condition=lambda q: "test" in q.query.lower(),
            model="gpt-4",
            priority=100
        )
        
        self.router.add_rule(rule)
        self.assertEqual(len(self.router.custom_rules), 1)

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```python
import pytest
from smartllm_router import SmartRouter

@pytest.fixture
def router():
    return SmartRouter(
        openai_key="test-key",
        strategy="balanced"
    )

def test_end_to_end_flow(router):
    """Test complete request flow"""
    response = router.chat.completions.create(
        model="auto",
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    assert response.content is not None
    assert response.model is not None
    assert response.cost >= 0
    assert response.savings >= 0

def test_analytics_tracking(router):
    """Test analytics are properly tracked"""
    # Make some requests
    for i in range(5):
        router.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": f"Query {i}"}]
        )
    
    analytics = router.get_analytics(period_days=1)
    assert analytics['total_requests'] == 5
    assert analytics['total_cost'] > 0
```

---

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV OPENAI_KEY=""
ENV ANTHROPIC_KEY=""

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartllm-router
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smartllm-router
  template:
    metadata:
      labels:
        app: smartllm-router
    spec:
      containers:
      - name: smartllm-router
        image: your-registry/smartllm-router:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-key
        - name: ANTHROPIC_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic-key
```

---

## 📞 Support & Resources

- **📖 Documentation:** [Full API Reference](API.md)
- **💬 Community:** [GitHub Discussions](https://github.com/yourusername/smartllm-router/discussions)
- **🐛 Issues:** [GitHub Issues](https://github.com/yourusername/smartllm-router/issues)
- **📧 Enterprise:** enterprise@smartllm-router.com

**Ready to start saving? [Install SmartLLM Router](../README.md#installation) today!**
