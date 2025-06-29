"""
Custom routing rules
"""

from typing import Callable
from dataclasses import dataclass


@dataclass
class RoutingRule:
    name: str
    condition: Callable[[object], bool]  # Takes QueryComplexity object
    model: str
    priority: int = 50
