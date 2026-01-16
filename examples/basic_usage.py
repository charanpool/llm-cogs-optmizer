import asyncio
import sys
import os

# Add src to path so we can import modules without installing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from providers.local import OllamaProvider
from providers.cloud import VertexAIProvider
from core.router import ModelRouter

async def main():
    print("Initializing LLM Cost Optimizer...")
    
    # 1. Setup Providers
    # In a real scenario, you'd pull these from env vars
    local = OllamaProvider(base_url="http://localhost:11434", model="llama3")
    
    # We use a dummy project ID here. If you have credentials, set them up.
    # The VertexAIProvider implementation handles missing libs gracefully-ish 
    # but actual calls would fail without auth.
    cloud = VertexAIProvider(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT", "demo-project"),
        location="us-central1"
    )

    # 2. Setup Router
    router = ModelRouter(local_provider=local, cloud_provider=cloud)

    # 3. Test Cases
    prompts = [
        "What is 2+2?",  # Simple -> Local
        "Explain the socioeconomic impact of the industrial revolution in 3 paragraphs.", # Complex -> Cloud (likely)
        "Write a python function to sort a list using quicksort." # Code -> Cloud (maybe)
    ]

    print(f"\n{'='*60}")
    print(f"{'Prompt':<40} | {'Route':<10} | {'Savings':<10}")
    print(f"{'-'*60}")

    for prompt in prompts:
        # In a real run without actual local/cloud access, this might fail on .generate()
        # So we'll mock the generation for this example if needed, 
        # but let's try to run the routing logic at least.
        
        # We can inspect the analyzer decision directly for demo purposes
        # to avoid needing a running Ollama instance for this script to just 'show' logic.
        
        is_cloud = router.analyzer.should_use_cloud(prompt)
        dest = "CLOUD" if is_cloud else "LOCAL"
        
        # Simulate cost
        cloud_cost = await cloud.estimate_cost(prompt)
        local_cost = await local.estimate_cost(prompt) # 0
        savings = cloud_cost - local_cost if not is_cloud else 0.0
        
        # Print summary
        display_prompt = (prompt[:37] + '...') if len(prompt) > 37 else prompt
        print(f"{display_prompt:<40} | {dest:<10} | ${savings:.6f}")

    print(f"{'='*60}\n")
    print("Note: This example demonstrates the routing logic. To execute actual calls, ensure Ollama is running and Cloud credentials are set.")

if __name__ == "__main__":
    asyncio.run(main())
