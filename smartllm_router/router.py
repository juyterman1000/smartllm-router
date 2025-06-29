"""
SmartLLM Router - Core implementation
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from .analyzer import QueryAnalyzer
from .selector import ModelSelector
from .tracker import CostTracker
from .rules import RoutingRule


@dataclass
class RouterResponse:
    content: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    cost: float
    savings: float
    latency: float
    quality_score: Optional[float] = None


class SmartRouter:
    """Main router class that orchestrates the routing logic"""

    def __init__(
        self,
        openai_key: Optional[str] = None,
        anthropic_key: Optional[str] = None,
        google_key: Optional[str] = None,
        mistral_key: Optional[str] = None,
        strategy: str = "balanced",
        daily_budget: Optional[float] = None,
        cache_ttl: int = 3600,
        enable_fallback: bool = True
    ):
        self.strategy = strategy
        self.daily_budget = daily_budget
        self.cache_ttl = cache_ttl
        self.enable_fallback = enable_fallback

        # Initialize components
        self.analyzer = QueryAnalyzer()
        self.selector = ModelSelector()
        self.tracker = CostTracker()

        # API keys
        self.api_keys = {
            "openai": openai_key,
            "anthropic": anthropic_key,
            "google": google_key,
            "mistral": mistral_key
        }

        # Custom routing rules
        self.custom_rules = []

        # Response cache
        self.cache = {}

        # Create a chat completions interface for compatibility
        self.chat = self
        self.completions = self

        logging.info("SmartRouter initialized with strategy: %s", strategy)

    def add_rule(self, rule: RoutingRule):
        """Add a custom routing rule"""
        self.custom_rules.append(rule)

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "auto",
        **kwargs
    ) -> RouterResponse:
        """Main entry point - compatible with OpenAI client interface"""

        # Extract the query from messages
        query = self._extract_query(messages)

        # Check cache first
        cache_key = self._generate_cache_key(query)
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if time.time() - cached["timestamp"] < self.cache_ttl:
                logging.info("Cache hit for query")
                return cached["response"]

        # Analyze query complexity
        complexity = self.analyzer.analyze(query)

        # Select optimal model
        if model == "auto":
            selected_model = self.selector.select_model(
                complexity,
                self.strategy,
                self.custom_rules
            )
        else:
            selected_model = self.selector.models.get(model)
            if not selected_model:
                raise ValueError(f"Unknown model: {model}")

        # Make the API call (placeholder for actual implementation)
        start_time = time.time()
        response_content = self._call_model_api(selected_model, messages, **kwargs)
        latency = time.time() - start_time

        # Calculate costs
        output_tokens = len(response_content) // 4  # Rough estimate
        actual_cost = self._calculate_cost(
            selected_model,
            complexity.token_count,
            output_tokens
        )

        # Calculate savings (compared to GPT-4)
        gpt4_cost = self._calculate_cost(
            self.selector.models["gpt-4"],
            complexity.token_count,
            output_tokens
        )
        savings = max(0, gpt4_cost - actual_cost)

        # Create response
        response = RouterResponse(
            content=response_content,
            model=selected_model.name,
            provider=selected_model.provider.value,
            input_tokens=complexity.token_count,
            output_tokens=output_tokens,
            cost=actual_cost,
            savings=savings,
            latency=latency
        )

        # Track the request
        self.tracker.track_request(
            model=selected_model.name,
            provider=selected_model.provider.value,
            input_tokens=complexity.token_count,
            output_tokens=output_tokens,
            cost=actual_cost,
            savings=savings,
            latency=latency
        )

        # Cache the response
        self.cache[cache_key] = {
            "response": response,
            "timestamp": time.time()
        }

        return response

    def _extract_query(self, messages: List[Dict[str, str]]) -> str:
        """Extract the user query from messages"""
        for message in reversed(messages):
            if message.get("role") == "user":
                return message.get("content", "")
        return ""

    def _generate_cache_key(self, query: str) -> str:
        """Generate a cache key for the query"""
        return str(hash(query))

    def _calculate_cost(self, model, input_tokens: int, output_tokens: int) -> float:
        """Calculate the cost for a request"""
        input_cost = (input_tokens / 1000) * model.cost_per_1k_input
        output_cost = (output_tokens / 1000) * model.cost_per_1k_output
        return input_cost + output_cost

    def _call_model_api(self, model, messages: List[Dict[str, str]], **kwargs) -> str:
        """Call the appropriate model API"""
        try:
            if model.provider.value == "openai":
                return self._call_openai_api(model, messages, **kwargs)
            elif model.provider.value == "anthropic":
                return self._call_anthropic_api(model, messages, **kwargs)
            elif model.provider.value == "google":
                return self._call_google_api(model, messages, **kwargs)
            elif model.provider.value == "mistral":
                return self._call_mistral_api(model, messages, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {model.provider.value}")
        except Exception as e:
            if self.enable_fallback:
                logging.warning(f"API call failed for {model.name}, falling back to GPT-3.5: {e}")
                return self._call_openai_api(self.selector.models["gpt-3.5-turbo"], messages, **kwargs)
            else:
                raise

    def _call_openai_api(self, model, messages: List[Dict[str, str]], **kwargs) -> str:
        """Call OpenAI API"""
        import openai

        if not self.api_keys["openai"]:
            raise ValueError("OpenAI API key not provided")

        client = openai.OpenAI(api_key=self.api_keys["openai"])

        response = client.chat.completions.create(
            model=model.name,
            messages=messages,
            **kwargs
        )

        return response.choices[0].message.content

    def _call_anthropic_api(self, model, messages: List[Dict[str, str]], **kwargs) -> str:
        """Call Anthropic API"""
        import anthropic

        if not self.api_keys["anthropic"]:
            raise ValueError("Anthropic API key not provided")

        client = anthropic.Anthropic(api_key=self.api_keys["anthropic"])

        # Convert OpenAI format to Anthropic format
        system_message = ""
        user_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)

        response = client.messages.create(
            model=model.name,
            max_tokens=kwargs.get("max_tokens", 1000),
            system=system_message,
            messages=user_messages
        )

        return response.content[0].text

    def _call_google_api(self, model, messages: List[Dict[str, str]], **kwargs) -> str:
        """Call Google Gemini API"""
        import google.generativeai as genai

        if not self.api_keys["google"]:
            raise ValueError("Google API key not provided")

        genai.configure(api_key=self.api_keys["google"])

        # Convert messages to Google format
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

        model_instance = genai.GenerativeModel(model.name)
        response = model_instance.generate_content(prompt)

        return response.text

    def _call_mistral_api(self, model, messages: List[Dict[str, str]], **kwargs) -> str:
        """Call Mistral API"""
        from mistralai.client import MistralClient
        from mistralai.models.chat_completion import ChatMessage

        if not self.api_keys["mistral"]:
            raise ValueError("Mistral API key not provided")

        client = MistralClient(api_key=self.api_keys["mistral"])

        # Convert to Mistral format
        mistral_messages = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in messages
        ]

        response = client.chat(
            model=model.name,
            messages=mistral_messages,
            **kwargs
        )

        return response.choices[0].message.content

    def get_analytics(self, period_days: int = 7) -> Dict[str, Any]:
        """Get usage analytics"""
        return self.tracker.get_analytics(period_days)
