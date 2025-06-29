"""
SmartLLM Router Demo Application
Interactive demo showcasing cost optimization capabilities
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
from datetime import datetime
import json

# Mock the router for demo purposes
class MockSmartRouter:
    """Mock router for demo purposes"""
    
    def __init__(self):
        self.requests_log = []
        
        # Model pricing (per 1K tokens)
        self.model_costs = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
            "gemini-pro": {"input": 0.0005, "output": 0.0015},
            "mistral-7b": {"input": 0.0002, "output": 0.0006}
        }
        
        # Model selection logic
        self.routing_rules = {
            "cost_optimized": {
                "simple": "mistral-7b",
                "medium": "claude-3-haiku", 
                "complex": "gpt-3.5-turbo"
            },
            "balanced": {
                "simple": "claude-3-haiku",
                "medium": "gpt-3.5-turbo",
                "complex": "gpt-4"
            },
            "quality_first": {
                "simple": "gpt-3.5-turbo",
                "medium": "gpt-4",
                "complex": "gpt-4"
            }
        }
    
    def analyze_query_complexity(self, query):
        """Analyze query complexity"""
        query_lower = query.lower()
        
        # Simple patterns
        simple_patterns = ["what is", "how many", "who is", "when did", "where is"]
        if any(pattern in query_lower for pattern in simple_patterns) and len(query) < 50:
            return "simple"
        
        # Complex patterns
        complex_patterns = ["analyze", "explain in detail", "write code", "implement", "debug", "compare and contrast"]
        if any(pattern in query_lower for pattern in complex_patterns) or len(query) > 200:
            return "complex"
        
        return "medium"
    
    def route_query(self, query, strategy="balanced"):
        """Route query and return response with cost analysis"""
        complexity = self.analyze_query_complexity(query)
        selected_model = self.routing_rules[strategy][complexity]
        
        # Simulate token counts
        input_tokens = len(query.split()) * 1.3  # Rough approximation
        output_tokens = input_tokens * 0.8  # Typical response ratio
        
        # Calculate costs
        model_cost = self.model_costs[selected_model]
        actual_cost = (input_tokens * model_cost["input"] + output_tokens * model_cost["output"]) / 1000
        
        # Calculate GPT-4 baseline cost for savings
        gpt4_cost = self.model_costs["gpt-4"]
        baseline_cost = (input_tokens * gpt4_cost["input"] + output_tokens * gpt4_cost["output"]) / 1000
        
        savings = max(0, baseline_cost - actual_cost)
        savings_percentage = (savings / baseline_cost * 100) if baseline_cost > 0 else 0
        
        # Generate mock response
        response_content = f"This is a {complexity} query routed to {selected_model}. " + \
                          f"The response demonstrates the model's capability to handle this type of request effectively."
        
        result = {
            "query": query,
            "complexity": complexity,
            "model": selected_model,
            "strategy": strategy,
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens),
            "cost": actual_cost,
            "baseline_cost": baseline_cost,
            "savings": savings,
            "savings_percentage": savings_percentage,
            "response": response_content,
            "timestamp": datetime.now()
        }
        
        self.requests_log.append(result)
        return result


def main():
    """Main demo application"""
    st.set_page_config(
        page_title="SmartLLM Router Demo",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 SmartLLM Router Interactive Demo")
    st.markdown("**Experience intelligent cost optimization for LLM APIs**")
    
    # Initialize router
    if 'router' not in st.session_state:
        st.session_state.router = MockSmartRouter()
    
    router = st.session_state.router
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    strategy = st.sidebar.selectbox(
        "Routing Strategy",
        ["cost_optimized", "balanced", "quality_first"],
        index=1,
        help="Choose how aggressively to optimize for cost vs quality"
    )
    
    # Strategy explanations
    strategy_info = {
        "cost_optimized": "🔥 **Cost Optimized**: Prioritizes cheapest models, uses premium models only when necessary",
        "balanced": "⚖️ **Balanced**: Balances cost and quality, good for most use cases", 
        "quality_first": "⭐ **Quality First**: Prioritizes best models, cost-conscious but quality-focused"
    }
    
    st.sidebar.info(strategy_info[strategy])
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Try It Out")
        
        # Predefined example queries
        example_queries = {
            "Simple Q&A": "What is the capital of France?",
            "Code Generation": "Write a Python function to implement binary search",
            "Analysis": "Analyze the pros and cons of remote work for software companies",
            "Creative Writing": "Write a short story about a robot learning to paint",
            "Math Problem": "Solve this equation: 2x + 5 = 15, and explain the steps"
        }
        
        st.subheader("📝 Example Queries")
        example_cols = st.columns(len(example_queries))
        
        for i, (category, query) in enumerate(example_queries.items()):
            with example_cols[i]:
                if st.button(category, key=f"example_{i}"):
                    st.session_state.current_query = query
        
        # Query input
        query = st.text_area(
            "Enter your query:",
            value=st.session_state.get('current_query', ''),
            height=100,
            placeholder="Ask anything... The router will automatically select the best model for cost and quality!"
        )
        
        if st.button("🚀 Route Query", type="primary", disabled=not query.strip()):
            with st.spinner("Analyzing query and routing to optimal model..."):
                time.sleep(1)  # Simulate processing time
                result = router.route_query(query, strategy)
                st.session_state.last_result = result
        
        # Display result
        if 'last_result' in st.session_state:
            result = st.session_state.last_result
            
            st.success("✅ Query processed successfully!")
            
            # Result metrics
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.metric(
                    "Model Selected",
                    result["model"],
                    help="The model chosen by SmartRouter"
                )
            
            with metric_cols[1]:
                st.metric(
                    "Cost",
                    f"${result['cost']:.4f}",
                    help="Actual cost for this query"
                )
            
            with metric_cols[2]:
                st.metric(
                    "Savings",
                    f"${result['savings']:.4f}",
                    f"{result['savings_percentage']:.1f}% vs GPT-4"
                )
            
            with metric_cols[3]:
                st.metric(
                    "Complexity",
                    result["complexity"].title(),
                    help="Detected query complexity level"
                )
            
            # Response
            st.subheader("📄 Response")
            st.write(result["response"])
    
    with col2:
        st.header("📊 Live Analytics")
        
        if router.requests_log:
            # Recent requests
            st.subheader("🕒 Recent Requests")
            recent_df = pd.DataFrame(router.requests_log[-5:])
            
            for _, row in recent_df.iterrows():
                with st.expander(f"{row['model']} - ${row['cost']:.4f}"):
                    st.write(f"**Query:** {row['query'][:100]}...")
                    st.write(f"**Complexity:** {row['complexity']}")
                    st.write(f"**Savings:** ${row['savings']:.4f} ({row['savings_percentage']:.1f}%)")
            
            # Cumulative savings
            total_savings = sum(r['savings'] for r in router.requests_log)
            total_cost = sum(r['cost'] for r in router.requests_log)
            total_baseline = sum(r['baseline_cost'] for r in router.requests_log)
            
            st.subheader("💰 Cumulative Savings")
            st.metric(
                "Total Saved",
                f"${total_savings:.4f}",
                f"{(total_savings/total_baseline*100):.1f}% reduction"
            )
            
            # Model usage chart
            if len(router.requests_log) > 1:
                st.subheader("🤖 Model Usage")
                model_counts = pd.Series([r['model'] for r in router.requests_log]).value_counts()
                
                fig = px.pie(
                    values=model_counts.values,
                    names=model_counts.index,
                    title="Model Distribution"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👆 Try some queries above to see analytics!")
    
    # Cost comparison section
    st.header("💡 Cost Comparison")
    
    if router.requests_log:
        comparison_data = []
        for req in router.requests_log:
            comparison_data.append({
                "Query": req['query'][:50] + "...",
                "SmartRouter Cost": req['cost'],
                "GPT-4 Cost": req['baseline_cost'],
                "Savings": req['savings']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='GPT-4 Baseline',
            x=comparison_df.index,
            y=comparison_df['GPT-4 Cost'],
            marker_color='red',
            opacity=0.7
        ))
        
        fig.add_trace(go.Bar(
            name='SmartRouter',
            x=comparison_df.index,
            y=comparison_df['SmartRouter Cost'],
            marker_color='green',
            opacity=0.7
        ))
        
        fig.update_layout(
            title='Cost Comparison: GPT-4 vs SmartRouter',
            xaxis_title='Query Number',
            yaxis_title='Cost ($)',
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **🚀 SmartLLM Router Demo**
    
    This demo shows how SmartLLM Router can reduce your LLM costs by 70-80% while maintaining quality.
    
    - **Intelligent Routing**: Automatically selects the best model for each query
    - **Cost Optimization**: Significant savings compared to always using premium models
    - **Quality Preservation**: Complex queries still get routed to capable models
    - **Real-time Analytics**: Track your savings and usage patterns
    
    Ready to integrate? Check out our [GitHub repository](https://github.com/yourusername/smartllm-router) for installation and setup instructions.
    """)


if __name__ == "__main__":
    main()
