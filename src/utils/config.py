from pydantic import BaseModel

class OptimizerConfig(BaseModel):
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    
    vertex_project_id: str = "my-project"
    vertex_location: str = "us-central1"
    vertex_model: str = "text-bison@001"
    
    complexity_threshold: int = 50
