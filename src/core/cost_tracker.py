import time
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class Transaction:
    timestamp: float
    provider_name: str
    prompt_length: int
    estimated_cost: float
    potential_cloud_cost: float # What it would have cost on cloud if routed locally

@dataclass
class CostStats:
    total_requests: int = 0
    total_cost: float = 0.0
    total_savings: float = 0.0

class CostTracker:
    """Tracks costs and savings."""

    def __init__(self):
        self.transactions: List[Transaction] = []

    def record_transaction(self, provider_name: str, prompt_length: int, actual_cost: float, cloud_cost_benchmark: float):
        savings = 0.0
        if provider_name != "cloud_benchmark": # If we didn't use the cloud benchmark
             savings = max(0, cloud_cost_benchmark - actual_cost)
        
        self.transactions.append(Transaction(
            timestamp=time.time(),
            provider_name=provider_name,
            prompt_length=prompt_length,
            estimated_cost=actual_cost,
            potential_cloud_cost=cloud_cost_benchmark
        ))

    def get_stats(self) -> CostStats:
        stats = CostStats()
        stats.total_requests = len(self.transactions)
        stats.total_cost = sum(t.estimated_cost for t in self.transactions)
        # Savings is the difference between what we would have paid on cloud vs what we paid
        # This assumes cloud is the 'standard' we are optimizing against.
        stats.total_savings = sum(max(0, t.potential_cloud_cost - t.estimated_cost) for t in self.transactions)
        return stats
