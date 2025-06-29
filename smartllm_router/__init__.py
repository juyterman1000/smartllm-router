"""
SmartLLM Router - Intelligent cost optimization for LLM APIs
"""

from .router import SmartRouter, RouterResponse
from .analyzer import QueryAnalyzer, QueryComplexity
from .selector import ModelSelector, Model, ModelProvider
from .tracker import CostTracker
from .rules import RoutingRule

__version__ = "0.1.0"
__all__ = [
    "SmartRouter",
    "RouterResponse",
    "QueryAnalyzer",
    "QueryComplexity",
    "ModelSelector",
    "Model",
    "ModelProvider",
    "CostTracker",
    "RoutingRule",
]
