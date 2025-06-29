"""
SmartLLM Router Benchmarking Tool
"""

import time
import json
import asyncio
import statistics
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse

from .router import SmartRouter
from .analyzer import QueryAnalyzer


@dataclass
class BenchmarkResult:
    query: str
    model_used: str
    provider: str
    latency: float
    cost: float
    savings: float
    quality_score: Optional[float] = None
    error: Optional[str] = None


@dataclass
class BenchmarkSuite:
    name: str
    description: str
    queries: List[str]
    expected_complexity: str  # "simple", "medium", "complex"


class LLMBenchmark:
    """Comprehensive benchmarking tool for SmartLLM Router"""
    
    def __init__(self, router: SmartRouter):
        self.router = router
        self.analyzer = QueryAnalyzer()
        
        # Predefined benchmark suites
        self.benchmark_suites = {
            "simple_qa": BenchmarkSuite(
                name="Simple Q&A",
                description="Basic factual questions that should route to cheaper models",
                queries=[
                    "What is the capital of France?",
                    "How many days are in a year?",
                    "What color is the sky?",
                    "Who wrote Romeo and Juliet?",
                    "What is 2 + 2?",
                    "What is the largest planet in our solar system?",
                    "How many continents are there?",
                    "What is the chemical symbol for water?",
                    "In what year did World War II end?",
                    "What is the speed of light?"
                ],
                expected_complexity="simple"
            ),
            
            "code_generation": BenchmarkSuite(
                name="Code Generation",
                description="Programming tasks that require more capable models",
                queries=[
                    "Write a Python function to implement quicksort",
                    "Create a React component for a todo list",
                    "Implement a binary search tree in JavaScript",
                    "Write a SQL query to find the top 10 customers by revenue",
                    "Create a REST API endpoint in Flask for user authentication",
                    "Implement a recursive fibonacci function with memoization",
                    "Write a regex pattern to validate email addresses",
                    "Create a Docker file for a Node.js application",
                    "Implement a simple blockchain in Python",
                    "Write unit tests for a calculator class"
                ],
                expected_complexity="complex"
            ),
            
            "analysis_reasoning": BenchmarkSuite(
                name="Analysis & Reasoning",
                description="Complex analytical tasks requiring advanced reasoning",
                queries=[
                    "Analyze the pros and cons of remote work for software companies",
                    "Explain the economic implications of artificial intelligence on job markets",
                    "Compare and contrast different machine learning algorithms for image classification",
                    "Discuss the ethical considerations of autonomous vehicles",
                    "Analyze the factors contributing to climate change and potential solutions",
                    "Evaluate the impact of social media on mental health",
                    "Explain the concept of quantum computing and its potential applications",
                    "Analyze the geopolitical implications of renewable energy adoption",
                    "Discuss the challenges and opportunities of space exploration",
                    "Evaluate different investment strategies for retirement planning"
                ],
                expected_complexity="complex"
            ),
            
            "creative_writing": BenchmarkSuite(
                name="Creative Writing",
                description="Creative tasks that benefit from advanced language models",
                queries=[
                    "Write a short story about a time traveler who gets stuck in the past",
                    "Create a poem about the beauty of nature in autumn",
                    "Write a product description for a revolutionary new smartphone",
                    "Create a compelling elevator pitch for a startup idea",
                    "Write a news article about a breakthrough in renewable energy",
                    "Create a character description for a fantasy novel protagonist",
                    "Write a persuasive essay about the importance of education",
                    "Create a script for a 30-second commercial about coffee",
                    "Write a technical blog post about microservices architecture",
                    "Create a social media campaign for a new fitness app"
                ],
                expected_complexity="medium"
            )
        }
    
    def run_single_query(self, query: str, strategy: str = "balanced") -> BenchmarkResult:
        """Run a single query benchmark"""
        try:
            start_time = time.time()
            
            response = self.router.chat.completions.create(
                model="auto",
                messages=[{"role": "user", "content": query}],
                strategy=strategy
            )
            
            latency = time.time() - start_time
            
            return BenchmarkResult(
                query=query,
                model_used=response.model,
                provider=response.provider,
                latency=latency,
                cost=response.cost,
                savings=response.savings,
                quality_score=response.quality_score
            )
            
        except Exception as e:
            return BenchmarkResult(
                query=query,
                model_used="error",
                provider="error",
                latency=0.0,
                cost=0.0,
                savings=0.0,
                error=str(e)
            )
    
    def run_suite(self, suite_name: str, strategy: str = "balanced") -> Dict[str, Any]:
        """Run a complete benchmark suite"""
        if suite_name not in self.benchmark_suites:
            raise ValueError(f"Unknown benchmark suite: {suite_name}")
        
        suite = self.benchmark_suites[suite_name]
        results = []
        
        print(f"\n🚀 Running benchmark suite: {suite.name}")
        print(f"📝 Description: {suite.description}")
        print(f"🎯 Strategy: {strategy}")
        print(f"📊 Queries: {len(suite.queries)}")
        print("-" * 60)
        
        for i, query in enumerate(suite.queries, 1):
            print(f"[{i}/{len(suite.queries)}] Running query: {query[:50]}...")
            
            result = self.run_single_query(query, strategy)
            results.append(result)
            
            if result.error:
                print(f"❌ Error: {result.error}")
            else:
                print(f"✅ Model: {result.model_used} | Cost: ${result.cost:.4f} | Savings: ${result.savings:.4f}")
        
        # Calculate summary statistics
        successful_results = [r for r in results if not r.error]
        
        if successful_results:
            total_cost = sum(r.cost for r in successful_results)
            total_savings = sum(r.savings for r in successful_results)
            avg_latency = statistics.mean(r.latency for r in successful_results)
            model_distribution = {}
            
            for result in successful_results:
                model_distribution[result.model_used] = model_distribution.get(result.model_used, 0) + 1
        else:
            total_cost = total_savings = avg_latency = 0
            model_distribution = {}
        
        summary = {
            "suite_name": suite.name,
            "strategy": strategy,
            "total_queries": len(suite.queries),
            "successful_queries": len(successful_results),
            "failed_queries": len(results) - len(successful_results),
            "total_cost": total_cost,
            "total_savings": total_savings,
            "cost_reduction_percentage": (total_savings / (total_cost + total_savings)) * 100 if (total_cost + total_savings) > 0 else 0,
            "average_latency": avg_latency,
            "model_distribution": model_distribution,
            "results": [asdict(r) for r in results],
            "timestamp": datetime.now().isoformat()
        }
        
        return summary
    
    def run_strategy_comparison(self, suite_name: str) -> Dict[str, Any]:
        """Compare all strategies on a benchmark suite"""
        strategies = ["cost_optimized", "balanced", "quality_first"]
        comparison_results = {}
        
        print(f"\n🔄 Running strategy comparison for suite: {suite_name}")
        print("=" * 60)
        
        for strategy in strategies:
            print(f"\n📊 Testing strategy: {strategy.upper()}")
            comparison_results[strategy] = self.run_suite(suite_name, strategy)
        
        # Generate comparison summary
        comparison_summary = {
            "suite_name": suite_name,
            "strategies_compared": strategies,
            "comparison_results": comparison_results,
            "summary": {
                "cost_comparison": {
                    strategy: results["total_cost"] 
                    for strategy, results in comparison_results.items()
                },
                "savings_comparison": {
                    strategy: results["total_savings"] 
                    for strategy, results in comparison_results.items()
                },
                "latency_comparison": {
                    strategy: results["average_latency"] 
                    for strategy, results in comparison_results.items()
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return comparison_summary
    
    def run_full_benchmark(self) -> Dict[str, Any]:
        """Run all benchmark suites with all strategies"""
        print("🚀 Starting comprehensive SmartLLM Router benchmark")
        print("=" * 80)
        
        full_results = {
            "benchmark_start": datetime.now().isoformat(),
            "suite_results": {},
            "strategy_comparisons": {}
        }
        
        # Run each suite with strategy comparison
        for suite_name in self.benchmark_suites.keys():
            print(f"\n🎯 Benchmarking suite: {suite_name}")
            comparison = self.run_strategy_comparison(suite_name)
            full_results["strategy_comparisons"][suite_name] = comparison
        
        full_results["benchmark_end"] = datetime.now().isoformat()
        
        # Generate overall summary
        self._print_benchmark_summary(full_results)
        
        return full_results
    
    def _print_benchmark_summary(self, results: Dict[str, Any]):
        """Print a comprehensive benchmark summary"""
        print("\n" + "=" * 80)
        print("📊 SMARTLLM ROUTER BENCHMARK SUMMARY")
        print("=" * 80)
        
        for suite_name, comparison in results["strategy_comparisons"].items():
            print(f"\n🎯 {suite_name.upper().replace('_', ' ')}")
            print("-" * 40)
            
            for strategy, strategy_results in comparison["comparison_results"].items():
                cost_reduction = strategy_results["cost_reduction_percentage"]
                avg_latency = strategy_results["average_latency"]
                total_cost = strategy_results["total_cost"]
                
                print(f"  {strategy:15} | Cost: ${total_cost:6.3f} | Savings: {cost_reduction:5.1f}% | Latency: {avg_latency:5.2f}s")
        
        print("\n" + "=" * 80)


def main():
    """CLI entry point for benchmarking"""
    parser = argparse.ArgumentParser(description="SmartLLM Router Benchmarking Tool")
    parser.add_argument("--suite", choices=["simple_qa", "code_generation", "analysis_reasoning", "creative_writing", "all"], 
                       default="all", help="Benchmark suite to run")
    parser.add_argument("--strategy", choices=["cost_optimized", "balanced", "quality_first", "compare"], 
                       default="compare", help="Routing strategy to test")
    parser.add_argument("--output", help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    # Initialize router (would need API keys in production)
    router = SmartRouter(
        openai_key="demo-key",  # Replace with actual keys
        strategy="balanced"
    )
    
    benchmark = LLMBenchmark(router)
    
    if args.suite == "all":
        results = benchmark.run_full_benchmark()
    elif args.strategy == "compare":
        results = benchmark.run_strategy_comparison(args.suite)
    else:
        results = benchmark.run_suite(args.suite, args.strategy)
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")


if __name__ == "__main__":
    main()
