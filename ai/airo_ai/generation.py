from dataclasses import dataclass
from .models import ModelRequest, ModelResponse, ModelProvider

@dataclass(frozen=True)
class GenerationResult:
    files: tuple[tuple[str,str],...]
    explanation: str

def build_request(prompt: str, context: str = "") -> ModelRequest:
    return ModelRequest(
        system="return structured implementation instructions. never invent files outside the requested project.",
        prompt=f"context:\n{context}\n\nrequest:\n{prompt}",
    )

def handle_response(response: ModelResponse) -> GenerationResult:
    return GenerationResult(files=(), explanation=response.text)
