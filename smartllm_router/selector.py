"""
Model selection logic
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from .analyzer import QueryComplexity
from .rules import RoutingRule


class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    MISTRAL = "mistral"


@dataclass
class Model:
    name: str
    provider: ModelProvider
    cost_per_1k_input: float
    cost_per_1k_output: float
    max_tokens: int
    speed_score: float  # 1-10, higher is faster
    quality_score: float  # 1-10, higher is better
    capabilities: List[str] = field(default_factory=list)


class ModelSelector:
    """Selects the optimal model based on query complexity and constraints"""

    def __init__(self):
        self.models = self._initialize_models()

    def _initialize_models(self) -> Dict[str, Model]:
        """Initialize available models with their characteristics"""
        return {
            "gpt-3.5-turbo": Model(
                name="gpt-3.5-turbo",
                provider=ModelProvider.OPENAI,
                cost_per_1k_input=0.0005,
                cost_per_1k_output=0.0015,
                max_tokens=4096,
                speed_score=9,
                quality_score=7,
                capabilities=["general", "code_generation", "summarization"]
            ),
            "gpt-4o-mini": Model(
                name="gpt-4o-mini",
                provider=ModelProvider.OPENAI,
                cost_per_1k_input=0.00015,
                cost_per_1k_output=0.0006,
                max_tokens=128000,
                speed_score=9,
                quality_score=9,
                capabilities=["general", "code_generation", "summarization", "reasoning"]
            ),
            "gpt-4": Model(
                name="gpt-4",
                provider=ModelProvider.OPENAI,
                cost_per_1k_input=0.03,
                cost_per_1k_output=0.06,
                max_tokens=8192,
                speed_score=6,
                quality_score=10,
                capabilities=["all"]
            ),
            "claude-3-haiku": Model(
                name="claude-3-haiku",
                provider=ModelProvider.ANTHROPIC,
                cost_per_1k_input=0.00025,
                cost_per_1k_output=0.00125,
                max_tokens=200000,
                speed_score=10,
                quality_score=7.5,
                capabilities=["general", "summarization", "long_context"]
            ),
            "claude-3-opus": Model(
                name="claude-3-opus",
                provider=ModelProvider.ANTHROPIC,
                cost_per_1k_input=0.015,
                cost_per_1k_output=0.075,
                max_tokens=200000,
                speed_score=5,
                quality_score=10,
                capabilities=["all"]
            ),
            "mistral-7b": Model(
                name="mistral-7b",
                provider=ModelProvider.MISTRAL,
                cost_per_1k_input=0.0002,
                cost_per_1k_output=0.0002,
                max_tokens=8192,
                speed_score=8,
                quality_score=6,
                capabilities=["general", "code_generation"]
            ),
            "gemini-pro": Model(
                name="gemini-pro",
                provider=ModelProvider.GOOGLE,
                cost_per_1k_input=0.00025,
                cost_per_1k_output=0.0005,
                max_tokens=32000,
                speed_score=8,
                quality_score=8,
                capabilities=["general", "code_generation", "mathematical_reasoning"]
            )
        }

    def select_model(
        self,
        complexity: QueryComplexity,
        strategy: str = "balanced",
        custom_rules: List[RoutingRule] = None
    ) -> Model:
        """Select the optimal model based on complexity and strategy"""

        # Apply custom rules first
        if custom_rules:
            for rule in sorted(custom_rules, key=lambda r: r.priority, reverse=True):
                if rule.condition(complexity):
                    if rule.model in self.models:
                        return self.models[rule.model]

        # Strategy-based selection
        if strategy == "cost_optimized":
            return self._select_cost_optimized(complexity)
        elif strategy == "quality_first":
            return self._select_quality_first(complexity)
        else:  # balanced
            return self._select_balanced(complexity)

    def _select_cost_optimized(self, complexity: QueryComplexity) -> Model:
        """Select the cheapest model that can handle the query"""

        if complexity.complexity_score < 0.3:
            return self.models["mistral-7b"]
        elif complexity.complexity_score < 0.5:
            return self.models["claude-3-haiku"]
        elif complexity.complexity_score < 0.7:
            return self.models["gpt-3.5-turbo"]
        elif complexity.complexity_score < 0.85:
            return self.models["gemini-pro"]
        else:
            return self.models["gpt-4"]

    def _select_quality_first(self, complexity: QueryComplexity) -> Model:
        """Select the best quality model within reason"""

        if complexity.complexity_score < 0.2:
            return self.models["gpt-3.5-turbo"]
        elif complexity.complexity_score < 0.6:
            return self.models["gemini-pro"]
        else:
            return self.models["gpt-4"]

    def _select_balanced(self, complexity: QueryComplexity) -> Model:
        """Balance between cost and quality"""

        # Special handling for specific capabilities
        if "code_generation" in complexity.required_capabilities:
            if complexity.complexity_score > 0.7:
                return self.models["gpt-4"]
            else:
                return self.models["gpt-3.5-turbo"]

        if "long_context" in complexity.required_capabilities:
            return self.models["claude-3-haiku"]

        if "mathematical_reasoning" in complexity.required_capabilities:
            if complexity.complexity_score > 0.6:
                return self.models["gpt-4"]
            else:
                return self.models["gemini-pro"]

        # Default selection based on complexity
        if complexity.complexity_score < 0.4:
            return self.models["claude-3-haiku"]
        elif complexity.complexity_score < 0.7:
            return self.models["gpt-3.5-turbo"]
        else:
            return self.models["gpt-4"]
