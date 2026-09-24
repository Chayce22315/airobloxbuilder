from dataclasses import dataclass, field
from typing import Protocol, Any

@dataclass(frozen=True)
class GenerationRequest:
    prompt: str
    system: str = ""
    model: str = ""
    temperature: float = 0.2
    max_tokens: int = 4096
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class GenerationResult:
    text: str
    model: str
    provider: str
    finish_reason: str = "stop"
    usage: dict[str, int] = field(default_factory=dict)

class ModelProvider(Protocol):
    name: str
    def generate(self, request: GenerationRequest) -> GenerationResult: ...

@dataclass
class ModelRegistry:
    providers: dict[str, ModelProvider] = field(default_factory=dict)

    def register(self, provider: ModelProvider) -> None:
        self.providers[provider.name] = provider

    def get(self, name: str) -> ModelProvider:
        if name not in self.providers:
            raise KeyError(f"model provider is not registered: {name}")
        return self.providers[name]

    def names(self) -> tuple[str, ...]:
        return tuple(self.providers)
