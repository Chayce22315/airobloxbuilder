from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ModelRequest:
    system: str
    prompt: str

@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str

class ModelProvider(Protocol):
    name: str
    def generate(self, request: ModelRequest) -> ModelResponse: ...

class OpenAICompatibleProvider:
    def __init__(self, endpoint: str, model: str):
        self.endpoint=endpoint.rstrip("/")
        self.model=model
    def generate(self, request: ModelRequest) -> ModelResponse:
        raise RuntimeError("network model transport is not configured yet; provide a concrete adapter")
