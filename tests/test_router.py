"""
Comprehensive test cases for SmartLLM Router
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from smartllm_router import SmartRouter, RoutingRule, QueryComplexity, RouterResponse, QueryAnalyzer, ModelSelector


class TestRouterInitialization:
    """Test router initialization and configuration"""

    def test_basic_initialization(self):
        """Test basic router initialization"""
        router = SmartRouter(
            openai_key="test-key",
            strategy="balanced"
        )

        assert router.strategy == "balanced"
        assert router.api_keys["openai"] == "test-key"
        assert router.enable_fallback is True
        assert router.cache_ttl == 3600

    def test_all_providers_initialization(self):
        """Test initialization with all providers"""
        router = SmartRouter(
            openai_key="openai-key",
            anthropic_key="anthropic-key",
            google_key="google-key",
            mistral_key="mistral-key",
            strategy="quality_first",
            daily_budget=100.0,
            cache_ttl=7200,
            enable_fallback=False
        )

        assert router.api_keys["openai"] == "openai-key"
        assert router.api_keys["anthropic"] == "anthropic-key"
        assert router.api_keys["google"] == "google-key"
        assert router.api_keys["mistral"] == "mistral-key"
        assert router.strategy == "quality_first"
        assert router.daily_budget == 100.0
        assert router.cache_ttl == 7200
        assert router.enable_fallback is False


class TestQueryAnalysis:
    """Test query complexity analysis"""

    def test_simple_query_analysis(self):
        """Test analysis of simple queries"""
        analyzer = QueryAnalyzer()

        simple_queries = [
            "What is the capital of France?",
            "How many days are in a year?",
            "What color is the sky?"
        ]

        for query in simple_queries:
            complexity = analyzer.analyze(query)
            assert complexity.task_type == "simple_qa"
            assert complexity.complexity_score < 0.5
            assert complexity.token_count > 0

    def test_code_query_analysis(self):
        """Test analysis of code-related queries"""
        analyzer = QueryAnalyzer()

        code_queries = [
            "Write a Python function to implement quicksort",
            "Create a React component for a todo list",
            "Debug this JavaScript code"
        ]

        for query in code_queries:
            complexity = analyzer.analyze(query)
            assert complexity.task_type == "code"
            assert "code_generation" in complexity.required_capabilities
            assert complexity.complexity_score > 0.6

    def test_complex_analysis_query(self):
        """Test analysis of complex analytical queries"""
        analyzer = QueryAnalyzer()

        complex_query = "Analyze the economic implications of artificial intelligence on job markets and provide a detailed assessment of potential solutions"
        complexity = analyzer.analyze(complex_query)

        assert complexity.task_type == "analysis"
        assert complexity.complexity_score > 0.7
        assert "complex_reasoning" in complexity.required_capabilities


class TestModelSelection:
    """Test model selection logic"""

    def test_cost_optimized_selection(self):
        """Test cost-optimized model selection"""
        selector = ModelSelector()

        # Simple query should select cheapest model
        simple_complexity = QueryComplexity(
            token_count=10,
            vocabulary_complexity=0.3,
            task_type="simple_qa",
            estimated_output_tokens=20,
            required_capabilities=[],
            complexity_score=0.2
        )

        selected_model = selector.select_model(simple_complexity, "cost_optimized")
        assert selected_model.name == "mistral-7b"

        # Complex query should still select a capable model
        complex_complexity = QueryComplexity(
            token_count=100,
            vocabulary_complexity=0.8,
            task_type="reasoning",
            estimated_output_tokens=200,
            required_capabilities=["complex_reasoning"],
            complexity_score=0.9
        )

        selected_model = selector.select_model(complex_complexity, "cost_optimized")
        assert selected_model.name == "gpt-4"

    def test_quality_first_selection(self):
        """Test quality-first model selection"""
        selector = ModelSelector()

        # Even simple queries should get decent models
        simple_complexity = QueryComplexity(
            token_count=10,
            vocabulary_complexity=0.3,
            task_type="simple_qa",
            estimated_output_tokens=20,
            required_capabilities=[],
            complexity_score=0.1
        )

        selected_model = selector.select_model(simple_complexity, "quality_first")
        assert selected_model.name == "gpt-3.5-turbo"

    def test_balanced_selection(self):
        """Test balanced model selection"""
        selector = ModelSelector()

        # Code generation should prefer GPT models
        code_complexity = QueryComplexity(
            token_count=50,
            vocabulary_complexity=0.6,
            task_type="code",
            estimated_output_tokens=100,
            required_capabilities=["code_generation"],
            complexity_score=0.8
        )

        selected_model = selector.select_model(code_complexity, "balanced")
        assert selected_model.name == "gpt-4"


class TestCustomRoutingRules:
    """Test custom routing rules functionality"""

    def test_add_custom_rule(self):
        """Test adding custom routing rules"""
        router = SmartRouter(strategy="balanced")

        rule = RoutingRule(
            name="test_rule",
            condition=lambda q: q.task_type == "code",
            model="gpt-4",
            priority=100
        )

        router.add_rule(rule)

        assert len(router.custom_rules) == 1
        assert router.custom_rules[0].name == "test_rule"
        assert router.custom_rules[0].model == "gpt-4"
        assert router.custom_rules[0].priority == 100


if __name__ == "__main__":
    pytest.main([__file__])
