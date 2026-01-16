import re

class QueryAnalyzer:
    """Analyzes query complexity to determine routing strategy."""

    def __init__(self, complexity_threshold: int = 50):
        # 0-100 scale, where > threshold implies cloud/complex
        self.complexity_threshold = complexity_threshold

    def analyze(self, prompt: str) -> int:
        """Returns a complexity score between 0 and 100."""
        score = 0
        
        # Heuristic 1: Length (longer prompts often need more context/reasoning)
        if len(prompt) > 500:
            score += 30
        elif len(prompt) > 100:
            score += 10

        # Heuristic 2: Keywords indicating complex tasks
        complex_keywords = [
            r"explain", r"reason", r"compare", r"contrast", 
            r"code", r"function", r"class", r"implement", 
            r"analysis", r"summary"
        ]
        
        for keyword in complex_keywords:
            if re.search(keyword, prompt, re.IGNORECASE):
                score += 15

        # Cap at 100
        return min(score, 100)

    def should_use_cloud(self, prompt: str) -> bool:
        return self.analyze(prompt) > self.complexity_threshold
