from typing import Optional
from ..providers.base import BaseProvider
from .analyzer import QueryAnalyzer
from .cost_tracker import CostTracker

class ModelRouter:
    """Routes queries between local and cloud providers."""

    def __init__(
        self, 
        local_provider: BaseProvider, 
        cloud_provider: BaseProvider,
        analyzer: Optional[QueryAnalyzer] = None,
        tracker: Optional[CostTracker] = None
    ):
        self.local = local_provider
        self.cloud = cloud_provider
        self.analyzer = analyzer or QueryAnalyzer()
        self.tracker = tracker or CostTracker()

    async def route(self, prompt: str, **kwargs) -> str:
        """
        Routes the prompt to the appropriate provider and returns the response.
        Also tracks cost metrics.
        """
        # 1. Analyze Complexity
        use_cloud = self.analyzer.should_use_cloud(prompt)
        
        # 2. Select Provider
        selected_provider = self.cloud if use_cloud else self.local
        
        # 3. Generate Response
        response = await selected_provider.generate(prompt, **kwargs)
        
        # 4. Calculate & Record Costs
        # We assume the cloud provider is the benchmark for 'potential cost'
        # If we routed to local, we saved the cloud cost.
        # If we routed to cloud, we paid the cloud cost (savings = 0).
        
        actual_cost = await selected_provider.estimate_cost(prompt)
        cloud_cost_benchmark = await self.cloud.estimate_cost(prompt)
        
        # Simple token estimation for record keeping
        prompt_len = len(prompt) 
        
        self.tracker.record_transaction(
            provider_name=selected_provider.name,
            prompt_length=prompt_len,
            actual_cost=actual_cost,
            cloud_cost_benchmark=cloud_cost_benchmark
        )
        
        return response

    def get_stats(self):
        return self.tracker.get_stats()
