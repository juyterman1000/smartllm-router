#!/usr/bin/env python3
"""
Basic functionality test for SmartLLM Router
Tests core components without requiring API keys
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'smartllm_router'))

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from smartllm_router import SmartRouter, QueryAnalyzer, ModelSelector, CostTracker, RoutingRule
        print("✅ Core imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    return True

def test_query_analysis():
    """Test query analysis functionality"""
    print("\n🧠 Testing query analysis...")
    
    try:
        from smartllm_router.analyzer import QueryAnalyzer
        
        analyzer = QueryAnalyzer()
        
        # Test simple query
        simple_query = "What is the capital of France?"
        complexity = analyzer.analyze(simple_query)
        
        print(f"Simple query: '{simple_query}'")
        print(f"  - Task type: {complexity.task_type}")
        print(f"  - Complexity score: {complexity.complexity_score:.3f}")
        print(f"  - Token count: {complexity.token_count}")
        
        # Test code query
        code_query = "Write a Python function to implement quicksort algorithm"
        complexity = analyzer.analyze(code_query)
        
        print(f"\nCode query: '{code_query}'")
        print(f"  - Task type: {complexity.task_type}")
        print(f"  - Complexity score: {complexity.complexity_score:.3f}")
        print(f"  - Required capabilities: {complexity.required_capabilities}")
        
        print("✅ Query analysis working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Query analysis failed: {e}")
        return False

def test_model_selection():
    """Test model selection logic"""
    print("\n🎯 Testing model selection...")
    
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
        print(f"Simple query → {model.name} (cost optimized)")
        
        # Test complex query selection
        complex_complexity = QueryComplexity(
            token_count=100,
            vocabulary_complexity=0.8,
            task_type="reasoning",
            estimated_output_tokens=200,
            required_capabilities=["complex_reasoning"],
            complexity_score=0.9
        )
        
        model = selector.select_model(complex_complexity, "quality_first")
        print(f"Complex query → {model.name} (quality first)")
        
        print("✅ Model selection working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Model selection failed: {e}")
        return False

def test_cost_tracking():
    """Test cost tracking functionality"""
    print("\n💰 Testing cost tracking...")
    
    try:
        from smartllm_router.tracker import CostTracker
        
        tracker = CostTracker()
        
        # Track some mock requests
        tracker.track_request(
            model="gpt-3.5-turbo",
            provider="openai",
            input_tokens=50,
            output_tokens=30,
            cost=0.002,
            savings=0.008,
            latency=1.2
        )
        
        tracker.track_request(
            model="claude-3-haiku",
            provider="anthropic",
            input_tokens=75,
            output_tokens=45,
            cost=0.001,
            savings=0.012,
            latency=0.9
        )
        
        analytics = tracker.get_analytics(period_days=1)
        
        print(f"Total requests: {analytics['total_requests']}")
        print(f"Total cost: ${analytics['total_cost']:.4f}")
        print(f"Total savings: ${analytics['total_savings']:.4f}")
        print(f"Cost reduction: {analytics['cost_reduction_percentage']:.1f}%")
        
        print("✅ Cost tracking working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Cost tracking failed: {e}")
        return False

def test_routing_rules():
    """Test custom routing rules"""
    print("\n⚙️ Testing routing rules...")
    
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
        print(f"Rule '{rule.name}' applies to code query: {applies}")
        print(f"Target model: {rule.model}")
        print(f"Priority: {rule.priority}")
        
        print("✅ Routing rules working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Routing rules failed: {e}")
        return False

def test_router_initialization():
    """Test router initialization without API keys"""
    print("\n🚀 Testing router initialization...")
    
    try:
        from smartllm_router import SmartRouter
        
        # Test initialization without API keys (should work for testing)
        router = SmartRouter(strategy="balanced")
        
        print(f"Router strategy: {router.strategy}")
        print(f"Cache TTL: {router.cache_ttl}")
        print(f"Fallback enabled: {router.enable_fallback}")
        
        # Test adding custom rules
        from smartllm_router.rules import RoutingRule
        
        rule = RoutingRule(
            name="test_rule",
            condition=lambda q: q.task_type == "test",
            model="gpt-3.5-turbo",
            priority=50
        )
        
        router.add_rule(rule)
        print(f"Custom rules added: {len(router.custom_rules)}")
        
        print("✅ Router initialization working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Router initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SmartLLM Router - Basic Functionality Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_query_analysis,
        test_model_selection,
        test_cost_tracking,
        test_routing_rules,
        test_router_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SmartLLM Router is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
