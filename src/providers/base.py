from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, name: str, cost_per_token: float = 0.0):
        self.name = name
        self.cost_per_token = cost_per_token

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generates text based on the prompt."""
        pass

    @abstractmethod
    async def get_token_count(self, text: str) -> int:
        """Estimates or calculates token count."""
        pass

    async def estimate_cost(self, prompt: str) -> float:
        """Estimates cost for the given prompt."""
        tokens = await self.get_token_count(prompt)
        return tokens * self.cost_per_token
