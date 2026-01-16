from typing import Optional
from .base import BaseProvider
try:
    from google.cloud import aiplatform
    from vertexai.preview.language_models import TextGenerationModel
    HAS_VERTEX = True
except ImportError:
    HAS_VERTEX = False

class VertexAIProvider(BaseProvider):
    """Provider for Google Cloud Vertex AI."""

    def __init__(self, project_id: str, location: str, model_name: str = "text-bison@001", cost_per_token: float = 0.0005):
        super().__init__(name="vertex_ai_cloud", cost_per_token=cost_per_token)
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self._model = None
        
        if HAS_VERTEX:
            aiplatform.init(project=project_id, location=location)

    @property
    def model(self):
        if not HAS_VERTEX:
            raise ImportError("google-cloud-aiplatform is not installed.")
        if self._model is None:
            self._model = TextGenerationModel.from_pretrained(self.model_name)
        return self._model

    async def generate(self, prompt: str, **kwargs) -> str:
        # Vertex AI calls are typically synchronous in the basic SDK, 
        # but can be wrapped or used with async transport.
        # For simplicity here, we'll run it directly (blocking) or would need an executor.
        # Ideally, use the async_generate_content if available in newer SDKs.
        
        # Note: This is a blocking call in this simplified version.
        try:
            response = self.model.predict(prompt, **kwargs)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Vertex AI generation failed: {e}")

    async def get_token_count(self, text: str) -> int:
        # Simple estimation or use a tokenizer
        return len(text) // 4
