"""
Basic tests for SmartLLM Router
Tests core functionality without requiring API keys
"""

import pytest
import os
import sys

# Add the smartllm_router to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'smartllm_router'))


def test_imports():
    """Test that all modules can be imported"""
    try:
        from smartllm_router import SmartRouter, QueryAnalyzer, ModelSelector, CostTracker, RoutingRule
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_query_analyzer():
    """Test query analysis functionality"""
    try:
        from smartllm_router.analyzer import QueryAnalyzer
        
        analyzer = QueryAnalyzer()
        
        # Test simple query
        simple_query = "What is the capital of France?"
        complexity = analyzer.analyze(simple_query)
        
        assert complexity.task_type is not None
        assert isinstance(complexity.complexity_score, float)
        assert 0 <= complexity.complexity_score <= 1
        assert complexity.token_count > 0
        
    except Exception as e:
        pytest.fail(f"Query analysis failed: {e}")


def test_model_selector():
    """Test model selection logic"""
    try:
        from smartllm_router.selector import ModelSelector
        from smartllm_router.analyzer import QueryComplexity
        
        selector = ModelSelector()
        
        # Test simple query selection
        simple_complexity = QueryComplexity(
            token_count=10,
            vocabulary_complexity=0.3,
            task_type="simple_qa",
            estimated_output_tokens=20,
            required_capabilities=[],
            complexity_score=0.2
        )
        
        model = selector.select_model(simple_complexity, "cost_optimized")
        assert model is not None
        assert model.name is not None
        
    except Exception as e:
        pytest.fail(f"Model selection failed: {e}")


def test_cost_tracker():
    """Test cost tracking functionality"""
    try:
        from smartllm_router.tracker import CostTracker
        
        tracker = CostTracker()
        
        # Track a mock request
        tracker.track_request(
            model="gpt-3.5-turbo",
            provider="openai",
            input_tokens=50,
            output_tokens=30,
            cost=0.002,
            savings=0.008,
            latency=1.2
        )
        
        analytics = tracker.get_analytics(period_days=1)
        
        assert analytics['total_requests'] == 1
        assert analytics['total_cost'] == 0.002
        assert analytics['total_savings'] == 0.008
        
    except Exception as e:
        pytest.fail(f"Cost tracking failed: {e}")


def test_routing_rules():
    """Test custom routing rules"""
    try:
        from smartllm_router.rules import RoutingRule
        from smartllm_router.analyzer import QueryComplexity
        
        # Create a custom rule
        rule = RoutingRule(
            name="code_to_gpt4",
            condition=lambda q: q.task_type == "code",
            model="gpt-4",
            priority=100
        )
        
        # Test the rule
        code_complexity = QueryComplexity(
            token_count=50,
            vocabulary_complexity=0.6,
            task_type="code",
            estimated_output_tokens=100,
            required_capabilities=["code_generation"],
            complexity_score=0.8
        )
        
        applies = rule.condition(code_complexity)
        assert applies == True
        assert rule.model == "gpt-4"
        assert rule.priority == 100
        
    except Exception as e:
        pytest.fail(f"Routing rules failed: {e}")


def test_router_initialization():
    """Test router initialization without API keys"""
    try:
        from smartllm_router import SmartRouter
        
        # Test initialization without API keys (should work for testing)
        router = SmartRouter(strategy="balanced")
        
        assert router.strategy == "balanced"
        assert router.cache_ttl > 0
        assert isinstance(router.enable_fallback, bool)
        
    except Exception as e:
        pytest.fail(f"Router initialization failed: {e}")


def test_router_custom_rules():
    """Test adding custom rules to router"""
    try:
        from smartllm_router import SmartRouter
        from smartllm_router.rules import RoutingRule
        
        router = SmartRouter(strategy="balanced")
        
        rule = RoutingRule(
            name="test_rule",
            condition=lambda q: q.task_type == "test",
            model="gpt-3.5-turbo",
            priority=50
        )
        
        router.add_rule(rule)
        assert len(router.custom_rules) == 1
        assert router.custom_rules[0].name == "test_rule"
        
    except Exception as e:
        pytest.fail(f"Custom rules test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
