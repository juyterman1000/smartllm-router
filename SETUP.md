# 🔧 SmartLLM Router Setup Guide

## 🚀 Quick Setup (2 minutes)

### 1. Install SmartLLM Router
```bash
pip install smartllm-router
```

### 2. Get Your API Keys

#### **OpenAI (Required)**
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Copy your key (starts with `sk-`)

#### **Other Providers (Optional)**
- **Anthropic**: [Console](https://console.anthropic.com/) → API Keys
- **Google AI**: [MakerSuite](https://makersuite.google.com/app/apikey)
- **Mistral**: [Console](https://console.mistral.ai/) → API Keys

### 3. Set Your API Key

#### **Option A: Environment Variable (Recommended)**
```bash
# Linux/Mac
export OPENAI_API_KEY="sk-your-actual-key-here"

# Windows
set OPENAI_API_KEY=sk-your-actual-key-here
```

#### **Option B: .env File**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys
OPENAI_API_KEY=sk-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

#### **Option C: In Code (Not Recommended for Production)**
```python
from smartllm_router import SmartRouter

router = SmartRouter(
    openai_key="sk-your-actual-key-here"
)
```

### 4. Test Your Setup
```python
from smartllm_router import SmartRouter

# Initialize router
router = SmartRouter()  # Uses environment variables

# Test with a simple query
response = router.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Hello, world!"}]
)

print(f"✅ Working! Response: {response.content}")
print(f"💰 Cost: ${response.cost:.6f}")
print(f"💸 Saved: ${response.savings:.6f}")
```

---

## 🔒 Security Best Practices

### **✅ DO:**
- Use environment variables for API keys
- Use `.env` files for local development
- Add `.env` to your `.gitignore`
- Rotate API keys regularly
- Use different keys for development/production

### **❌ DON'T:**
- Commit API keys to version control
- Share API keys in chat/email
- Use production keys in development
- Hard-code keys in your source code

---

## 🎯 Configuration Options

### **Basic Configuration**
```python
from smartllm_router import SmartRouter

router = SmartRouter(
    openai_key=os.getenv("OPENAI_API_KEY"),
    strategy="balanced",  # "cost_optimized", "balanced", "quality_first"
    daily_budget=100.0,   # Optional budget limit
    cache_ttl=3600,       # Cache responses for 1 hour
    enable_fallback=True  # Fallback to GPT-3.5 on errors
)
```

### **Multi-Provider Configuration**
```python
router = SmartRouter(
    openai_key=os.getenv("OPENAI_API_KEY"),
    anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
    google_key=os.getenv("GOOGLE_API_KEY"),
    mistral_key=os.getenv("MISTRAL_API_KEY"),
    strategy="cost_optimized"
)
```

### **Enterprise Configuration**
```python
from smartllm_router import SmartRouter, RoutingRule

router = SmartRouter(
    openai_key=os.getenv("OPENAI_API_KEY"),
    strategy="balanced",
    daily_budget=1000.0,
    enable_fallback=True
)

# Add custom business rules
router.add_rule(RoutingRule(
    name="sensitive_to_gpt4",
    condition=lambda q: "confidential" in q.query.lower(),
    model="gpt-4",
    priority=100
))
```

---

## 🧪 Testing Your Setup

### **Run the Test Suite**
```bash
# Basic functionality test
python test_basic_functionality.py

# Real API test (requires API key)
python test_real_openai_only.py

# Use case tests
python test_real_world_use_cases.py
```

### **Expected Output**
```
🚀 SmartLLM Router - Real OpenAI API Test
✅ Direct API call successful!
✅ Model used: gpt-4o-mini
💰 Cost: $0.000015
🎉 Saved: $0.000585
```

---

## 🚨 Troubleshooting

### **"API key not provided" Error**
```python
# Check if your key is set
import os
print(os.getenv("OPENAI_API_KEY"))

# If None, set it:
export OPENAI_API_KEY="sk-your-key"
```

### **"Invalid API key" Error**
- Verify your key is correct
- Check if you have credits in your OpenAI account
- Make sure the key hasn't expired

### **"Module not found" Error**
```bash
# Install missing dependencies
pip install openai anthropic google-generativeai mistralai
```

### **Import Errors**
```bash
# Reinstall SmartLLM Router
pip uninstall smartllm-router
pip install smartllm-router
```

---

## 📊 Monitoring Your Usage

### **Check Your Costs**
```python
# Get analytics
analytics = router.get_analytics(period_days=7)
print(f"Weekly cost: ${analytics['total_cost']:.4f}")
print(f"Weekly savings: ${analytics['total_savings']:.4f}")
```

### **Set Budget Alerts**
```python
# Check daily spending
daily_cost = router.tracker.get_daily_cost()
if daily_cost > 50.0:
    print("⚠️ Daily budget exceeded!")
```

---

## 🎯 Next Steps

1. **📖 Read the [Integration Guide](docs/INTEGRATION.md)**
2. **💡 Check out [Real-World Examples](examples/)**
3. **📊 Try the [Interactive Demo](https://smartllm-demo.streamlit.app)**
4. **🤝 Join our [Community](https://github.com/yourusername/smartllm-router/discussions)**

---

## 💬 Need Help?

- **📖 Documentation**: [docs/](docs/)
- **💬 Community**: [GitHub Discussions](https://github.com/yourusername/smartllm-router/discussions)
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/yourusername/smartllm-router/issues)
- **📧 Enterprise Support**: enterprise@smartllm-router.com

**Happy cost optimizing! 💰🚀**
