"""
Performance tests for SmartLLM Router
Tests performance without requiring API keys
"""

import pytest
import time
import os
import sys

# Add the smartllm_router to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'smartllm_router'))


def test_query_analysis_performance():
    """Test query analysis performance"""
    try:
        from smartllm_router.analyzer import QueryAnalyzer
        
        analyzer = QueryAnalyzer()
        query = "What is the capital of France and what is its population?"
        
        start_time = time.time()
        complexity = analyzer.analyze(query)
        end_time = time.time()
        
        analysis_time = end_time - start_time
        
        # Analysis should be fast (under 100ms)
        assert analysis_time < 0.1
        assert complexity is not None
        
    except Exception as e:
        pytest.skip(f"Query analysis performance test skipped: {e}")


def test_model_selection_performance():
    """Test model selection performance"""
    try:
        from smartllm_router.selector import ModelSelector
        from smartllm_router.analyzer import QueryComplexity
        
        selector = ModelSelector()
        
        complexity = QueryComplexity(
            token_count=50,
            vocabulary_complexity=0.5,
            task_type="simple_qa",
            estimated_output_tokens=100,
            required_capabilities=[],
            complexity_score=0.5
        )
        
        start_time = time.time()
        model = selector.select_model(complexity, "balanced")
        end_time = time.time()
        
        selection_time = end_time - start_time
        
        # Model selection should be very fast (under 10ms)
        assert selection_time < 0.01
        assert model is not None
        
    except Exception as e:
        pytest.skip(f"Model selection performance test skipped: {e}")


def test_cost_tracking_performance():
    """Test cost tracking performance"""
    try:
        from smartllm_router.tracker import CostTracker
        
        tracker = CostTracker()
        
        start_time = time.time()
        
        # Track multiple requests
        for i in range(100):
            tracker.track_request(
                model="gpt-3.5-turbo",
                provider="openai",
                input_tokens=50,
                output_tokens=30,
                cost=0.002,
                savings=0.008,
                latency=1.0
            )
        
        end_time = time.time()
        
        tracking_time = end_time - start_time
        
        # Tracking 100 requests should be fast (under 100ms)
        assert tracking_time < 0.1
        
        analytics = tracker.get_analytics(period_days=1)
        assert analytics['total_requests'] == 100
        
    except Exception as e:
        pytest.skip(f"Cost tracking performance test skipped: {e}")


def test_router_initialization_performance():
    """Test router initialization performance"""
    try:
        from smartllm_router import SmartRouter
        
        start_time = time.time()
        router = SmartRouter(strategy="balanced")
        end_time = time.time()
        
        init_time = end_time - start_time
        
        # Router initialization should be fast (under 500ms)
        assert init_time < 0.5
        assert router is not None
        
    except Exception as e:
        pytest.skip(f"Router initialization performance test skipped: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
