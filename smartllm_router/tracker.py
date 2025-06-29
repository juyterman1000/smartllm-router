"""
Cost tracking and analytics
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics


class CostTracker:
    """Tracks costs and generates analytics"""

    def __init__(self):
        self.requests = []
        self.daily_costs = defaultdict(float)
        self.model_usage = defaultdict(int)
        self.total_savings = 0.0

    def track_request(
        self,
        model: str,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        savings: float,
        latency: float,
        timestamp: Optional[datetime] = None
    ):
        """Track a single request"""

        if timestamp is None:
            timestamp = datetime.now()

        request_data = {
            "timestamp": timestamp,
            "model": model,
            "provider": provider,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "savings": savings,
            "latency": latency
        }

        self.requests.append(request_data)
        self.daily_costs[timestamp.date()] += cost
        self.model_usage[model] += 1
        self.total_savings += savings

    def get_analytics(self, period_days: int = 7) -> Dict[str, Any]:
        """Get analytics for the specified period"""

        cutoff = datetime.now() - timedelta(days=period_days)
        recent_requests = [r for r in self.requests if r["timestamp"] > cutoff]

        if not recent_requests:
            return {
                "total_requests": 0,
                "total_cost": 0,
                "total_savings": 0,
                "average_latency": 0,
                "model_distribution": {},
                "daily_costs": {}
            }

        total_cost = sum(r["cost"] for r in recent_requests)
        total_savings = sum(r["savings"] for r in recent_requests)
        avg_latency = statistics.mean([r["latency"] for r in recent_requests])

        model_dist = defaultdict(int)
        for r in recent_requests:
            model_dist[r["model"]] += 1

        return {
            "total_requests": len(recent_requests),
            "total_cost": round(total_cost, 4),
            "total_savings": round(total_savings, 4),
            "cost_reduction_percentage": round((total_savings / (total_cost + total_savings)) * 100, 2) if (total_cost + total_savings) > 0 else 0,
            "average_latency": round(avg_latency, 3),
            "model_distribution": dict(model_dist),
            "daily_costs": {
                str(date): round(cost, 4)
                for date, cost in self.daily_costs.items()
                if date > cutoff.date()
            }
        }

    def get_daily_cost(self) -> float:
        """Get total cost for today"""
        today = datetime.now().date()
        daily_requests = [
            req for req in self.requests
            if req['timestamp'].date() == today
        ]
        return sum(req['cost'] for req in daily_requests)
