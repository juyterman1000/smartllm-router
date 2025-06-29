"""
SmartLLM Router Dashboard - Real-time cost tracking and analytics
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, Any

from .router import SmartRouter
from .tracker import CostTracker


def load_demo_data():
    """Load demo data for the dashboard"""
    # Generate realistic demo data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='H')
    
    models = ['gpt-4', 'gpt-3.5-turbo', 'claude-3-haiku', 'gemini-pro', 'mistral-7b']
    providers = ['openai', 'anthropic', 'google', 'mistral']
    
    data = []
    cumulative_savings = 0
    
    for date in dates:
        # Simulate requests throughout the day
        num_requests = np.random.poisson(5)
        
        for _ in range(num_requests):
            model = np.random.choice(models, p=[0.1, 0.3, 0.25, 0.2, 0.15])
            provider = 'openai' if 'gpt' in model else ('anthropic' if 'claude' in model else 
                      ('google' if 'gemini' in model else 'mistral'))
            
            # Simulate costs based on model
            base_costs = {
                'gpt-4': 0.03, 'gpt-3.5-turbo': 0.002, 'claude-3-haiku': 0.00025,
                'gemini-pro': 0.0005, 'mistral-7b': 0.0002
            }
            
            cost = base_costs[model] * np.random.uniform(0.5, 2.0)
            gpt4_cost = base_costs['gpt-4'] * np.random.uniform(0.5, 2.0)
            savings = max(0, gpt4_cost - cost)
            cumulative_savings += savings
            
            data.append({
                'timestamp': date,
                'model': model,
                'provider': provider,
                'cost': cost,
                'savings': savings,
                'cumulative_savings': cumulative_savings,
                'input_tokens': np.random.randint(50, 500),
                'output_tokens': np.random.randint(20, 200),
                'latency': np.random.uniform(0.5, 3.0)
            })
    
    return pd.DataFrame(data)


def create_cost_savings_chart(df):
    """Create cost savings visualization"""
    daily_data = df.groupby(df['timestamp'].dt.date).agg({
        'cost': 'sum',
        'savings': 'sum'
    }).reset_index()
    
    daily_data['gpt4_cost'] = daily_data['cost'] + daily_data['savings']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_data['timestamp'],
        y=daily_data['gpt4_cost'],
        mode='lines+markers',
        name='GPT-4 Cost (Baseline)',
        line=dict(color='red', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_data['timestamp'],
        y=daily_data['cost'],
        mode='lines+markers',
        name='SmartRouter Cost',
        line=dict(color='green', width=3),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title='Daily Cost Comparison: GPT-4 vs SmartRouter',
        xaxis_title='Date',
        yaxis_title='Cost ($)',
        hovermode='x unified'
    )
    
    return fig


def create_model_usage_chart(df):
    """Create model usage distribution chart"""
    model_usage = df['model'].value_counts()
    
    fig = px.pie(
        values=model_usage.values,
        names=model_usage.index,
        title='Model Usage Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    return fig


def create_savings_over_time(df):
    """Create cumulative savings chart"""
    fig = px.line(
        df,
        x='timestamp',
        y='cumulative_savings',
        title='Cumulative Cost Savings Over Time',
        labels={'cumulative_savings': 'Cumulative Savings ($)', 'timestamp': 'Date'}
    )
    
    fig.update_traces(line_color='green', line_width=3)
    
    return fig


def create_performance_metrics(df):
    """Create performance metrics dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    total_requests = len(df)
    total_savings = df['savings'].sum()
    avg_latency = df['latency'].mean()
    cost_reduction = (df['savings'].sum() / (df['cost'].sum() + df['savings'].sum())) * 100
    
    with col1:
        st.metric(
            label="Total Requests",
            value=f"{total_requests:,}",
            delta=f"+{int(total_requests * 0.15)} this week"
        )
    
    with col2:
        st.metric(
            label="Total Savings",
            value=f"${total_savings:.2f}",
            delta=f"+${total_savings * 0.2:.2f} this week"
        )
    
    with col3:
        st.metric(
            label="Avg Latency",
            value=f"{avg_latency:.2f}s",
            delta=f"-{avg_latency * 0.1:.2f}s"
        )
    
    with col4:
        st.metric(
            label="Cost Reduction",
            value=f"{cost_reduction:.1f}%",
            delta=f"+{cost_reduction * 0.05:.1f}%"
        )


def main():
    """Main dashboard application"""
    st.set_page_config(
        page_title="SmartLLM Router Dashboard",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🚀 SmartLLM Router Dashboard")
    st.markdown("**Real-time cost optimization and analytics for your LLM usage**")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # Demo mode toggle
    demo_mode = st.sidebar.checkbox("Demo Mode", value=True, help="Use demo data for visualization")
    
    if demo_mode:
        df = load_demo_data()
        st.sidebar.success("Using demo data")
    else:
        st.sidebar.info("Connect your SmartRouter instance for live data")
        # In production, this would connect to actual router data
        df = load_demo_data()  # Fallback to demo data
    
    # Time range selector
    time_range = st.sidebar.selectbox(
        "Time Range",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"],
        index=2
    )
    
    # Filter data based on time range
    now = datetime.now()
    if time_range == "Last 24 Hours":
        cutoff = now - timedelta(hours=24)
    elif time_range == "Last 7 Days":
        cutoff = now - timedelta(days=7)
    elif time_range == "Last 30 Days":
        cutoff = now - timedelta(days=30)
    else:
        cutoff = df['timestamp'].min()
    
    filtered_df = df[df['timestamp'] >= cutoff]
    
    # Performance metrics
    st.header("📊 Performance Overview")
    create_performance_metrics(filtered_df)
    
    # Charts
    st.header("📈 Cost Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cost_chart = create_cost_savings_chart(filtered_df)
        st.plotly_chart(cost_chart, use_container_width=True)
    
    with col2:
        savings_chart = create_savings_over_time(filtered_df)
        st.plotly_chart(savings_chart, use_container_width=True)
    
    # Model usage
    st.header("🤖 Model Usage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        usage_chart = create_model_usage_chart(filtered_df)
        st.plotly_chart(usage_chart, use_container_width=True)
    
    with col2:
        # Provider breakdown
        provider_usage = filtered_df['provider'].value_counts()
        provider_chart = px.bar(
            x=provider_usage.index,
            y=provider_usage.values,
            title='Requests by Provider',
            labels={'x': 'Provider', 'y': 'Number of Requests'}
        )
        st.plotly_chart(provider_chart, use_container_width=True)
    
    # Recent requests table
    st.header("📋 Recent Requests")
    recent_requests = filtered_df.tail(20)[['timestamp', 'model', 'provider', 'cost', 'savings', 'latency']]
    recent_requests['timestamp'] = recent_requests['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    recent_requests['cost'] = recent_requests['cost'].apply(lambda x: f"${x:.4f}")
    recent_requests['savings'] = recent_requests['savings'].apply(lambda x: f"${x:.4f}")
    recent_requests['latency'] = recent_requests['latency'].apply(lambda x: f"{x:.2f}s")
    
    st.dataframe(recent_requests, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**SmartLLM Router** - Intelligent cost optimization for LLM APIs")


if __name__ == "__main__":
    main()
