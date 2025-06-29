"""
Basic usage example for SmartLLM Router
"""

from smartllm_router import SmartRouter, RoutingRule


def main():
    # Initialize router
    router = SmartRouter(
        openai_key="sk-...",  # Add your keys here
        anthropic_key="sk-ant-...",
        strategy="cost_optimized"
    )
    
    # Example 1: Simple query
    print("Example 1: Simple Query")
    print("-" * 50)
    
    response = router.chat.completions.create(
        model="auto",
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    
    print(f"Query: What is the capital of France?")
    print(f"Model used: {response.model}")
    print(f"Cost: ${response.cost:.4f}")
    print(f"Saved: ${response.savings:.4f}")
    print(f"Response: {response.content}")
    print()
    
    # Example 2: Complex query
    print("Example 2: Complex Query")
    print("-" * 50)
    
    response = router.chat.completions.create(
        model="auto",
        messages=[
            {"role": "user", "content": "Write a Python function to implement quicksort"}
        ]
    )
    
    print(f"Query: Write a Python function to implement quicksort")
    print(f"Model used: {response.model}")
    print(f"Cost: ${response.cost:.4f}")
    print(f"Saved: ${response.savings:.4f}")
    print()
    
    # Example 3: Custom routing rule
    print("Example 3: Custom Routing Rule")
    print("-" * 50)
    
    # Add a rule to always use GPT-4 for code
    router.add_rule(
        RoutingRule(
            name="code_to_gpt4",
            condition=lambda q: q.task_type == "code",
            model="gpt-4",
            priority=100
        )
    )
    
    response = router.chat.completions.create(
        model="auto",
        messages=[
            {"role": "user", "content": "Debug this Python code: print(hello world)"}
        ]
    )
    
    print(f"Query: Debug this Python code...")
    print(f"Model used: {response.model} (forced by custom rule)")
    print()
    
    # Example 4: Analytics
    print("Example 4: Analytics")
    print("-" * 50)
    
    analytics = router.get_analytics(period_days=1)
    print(f"Total requests: {analytics['total_requests']}")
    print(f"Total cost: ${analytics['total_cost']:.2f}")
    print(f"Total savings: ${analytics['total_savings']:.2f}")
    print(f"Model distribution: {analytics['model_distribution']}")


if __name__ == "__main__":
    main()
