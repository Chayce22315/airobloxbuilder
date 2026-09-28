from dataclasses import dataclass
from typing import Iterable, Protocol

@dataclass(frozen=True)
class ProviderRequest:
    prompt: str
    system: str = ""

@dataclass(frozen=True)
class ProviderEvent:
    type: str
    text: str = ""

class ModelProvider(Protocol):
    def generate(self, request: ProviderRequest) -> Iterable[ProviderEvent]: ...

class EchoProvider:
    """Deterministic provider used by tests and offline development."""
    def generate(self, request: ProviderRequest) -> Iterable[ProviderEvent]:
        yield ProviderEvent("start")
        yield ProviderEvent("text", f"offline model response: {request.prompt}")
        yield ProviderEvent("complete")
