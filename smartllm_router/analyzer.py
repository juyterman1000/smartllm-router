"""
Query analysis module for complexity detection
"""

import re
from typing import List
from dataclasses import dataclass
import tiktoken


@dataclass
class QueryComplexity:
    token_count: int
    vocabulary_complexity: float
    task_type: str
    estimated_output_tokens: int
    required_capabilities: List[str]
    complexity_score: float


class QueryAnalyzer:
    """Analyzes query complexity to determine optimal model routing"""
    
    def __init__(self):
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
        # Task patterns
        self.task_patterns = {
            "simple_qa": [
                r"what is|what are|who is|who are|when is|when was|where is",
                r"define|definition of|meaning of",
                r"yes or no|true or false"
            ],
            "summarization": [
                r"summarize|summary of|tldr|key points",
                r"main idea|brief overview|condensed version"
            ],
            "code": [
                r"```|code|function|implement|algorithm|debug|fix",
                r"python|javascript|java|c\+\+|sql|programming"
            ],
            "analysis": [
                r"analyze|analysis|compare|contrast|evaluate",
                r"pros and cons|advantages|disadvantages|implications"
            ],
            "creative": [
                r"write a story|poem|creative|imagine|fictional",
                r"brainstorm|ideas for|suggestions for"
            ],
            "math": [
                r"calculate|solve|equation|formula|mathematical",
                r"derivative|integral|probability|statistics"
            ],
            "reasoning": [
                r"explain why|how does|logical|reasoning|think through",
                r"step by step|walkthrough|systematic"
            ]
        }
        
    def analyze(self, query: str) -> QueryComplexity:
        """Analyze query to determine complexity and routing requirements"""
        
        # Token analysis
        tokens = self.encoder.encode(query)
        token_count = len(tokens)
        
        # Vocabulary complexity
        unique_tokens = len(set(tokens))
        vocabulary_complexity = unique_tokens / token_count if token_count > 0 else 0
        
        # Detect task type
        task_type = self._detect_task_type(query)
        
        # Estimate output tokens
        estimated_output = self._estimate_output_tokens(task_type, token_count)
        
        # Determine required capabilities
        capabilities = self._detect_required_capabilities(query, task_type)
        
        # Calculate overall complexity score
        complexity_score = self._calculate_complexity_score(
            token_count, vocabulary_complexity, task_type, capabilities
        )
        
        return QueryComplexity(
            token_count=token_count,
            vocabulary_complexity=vocabulary_complexity,
            task_type=task_type,
            estimated_output_tokens=estimated_output,
            required_capabilities=capabilities,
            complexity_score=complexity_score
        )
    
    def _detect_task_type(self, query: str) -> str:
        """Detect the primary task type from the query"""
        query_lower = query.lower()
        
        for task_type, patterns in self.task_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return task_type
        
        return "general"
    
    def _estimate_output_tokens(self, task_type: str, input_tokens: int) -> int:
        """Estimate expected output tokens based on task type"""
        multipliers = {
            "simple_qa": 0.5,
            "summarization": 0.3,
            "code": 2.5,
            "analysis": 2.0,
            "creative": 3.0,
            "math": 1.5,
            "reasoning": 2.0,
            "general": 1.0
        }
        
        base_output = input_tokens * multipliers.get(task_type, 1.0)
        return int(base_output)
    
    def _detect_required_capabilities(self, query: str, task_type: str) -> List[str]:
        """Detect special capabilities required for the query"""
        capabilities = []
        
        if task_type == "code":
            capabilities.append("code_generation")
        if task_type == "math" or re.search(r'\d+[\+\-\*/]\d+', query):
            capabilities.append("mathematical_reasoning")
        if task_type in ["analysis", "reasoning"]:
            capabilities.append("complex_reasoning")
        if len(query) > 1000:
            capabilities.append("long_context")
        if re.search(r'json|xml|yaml|csv', query.lower()):
            capabilities.append("structured_output")
            
        return capabilities
    
    def _calculate_complexity_score(
        self, 
        token_count: int, 
        vocab_complexity: float,
        task_type: str,
        capabilities: List[str]
    ) -> float:
        """Calculate overall complexity score (0-1)"""
        
        # Base scores for different factors
        token_score = min(token_count / 500, 1.0) * 0.2
        vocab_score = vocab_complexity * 0.2
        
        # Task complexity scores
        task_scores = {
            "simple_qa": 0.1,
            "summarization": 0.3,
            "code": 0.8,
            "analysis": 0.7,
            "creative": 0.6,
            "math": 0.8,
            "reasoning": 0.9,
            "general": 0.5
        }
        task_score = task_scores.get(task_type, 0.5) * 0.4
        
        # Capability requirements score
        capability_score = min(len(capabilities) * 0.1, 0.2)
        
        return token_score + vocab_score + task_score + capability_score
