import httpx
from .base import BaseProvider

class OllamaProvider(BaseProvider):
    """Provider for local Ollama instances."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        super().__init__(name="ollama_local", cost_per_token=0.0)
        self.base_url = base_url
        self.model = model

    async def generate(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            # Merge additional kwargs into payload
            payload.update(kwargs)
            
            try:
                response = await client.post(f"{self.base_url}/api/generate", json=payload, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
            except Exception as e:
                # Fallback or re-raise depending on policy
                raise RuntimeError(f"Ollama generation failed: {e}")

    async def get_token_count(self, text: str) -> int:
        # Simple estimation: 1 token ~= 4 chars
        return len(text) // 4
