from dataclasses import dataclass
from typing import Iterable, Protocol
import json
import os
import urllib.error
import urllib.request

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
    """Deterministic provider used only for tests and offline development."""
    def generate(self, request: ProviderRequest) -> Iterable[ProviderEvent]:
        yield ProviderEvent("start")
        yield ProviderEvent("text", f"offline model response: {request.prompt}")
        yield ProviderEvent("complete")

class OpenAICompatibleProvider:
    """Calls any OpenAI-compatible /chat/completions endpoint.

    Configuration comes from AIRO_API_URL, AIRO_API_KEY and AIRO_MODEL.
    This keeps model weights and credentials outside the app.
    """
    def __init__(self, base_url: str, api_key: str, model: str, timeout: int = 120) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    @classmethod
    def from_environment(cls) -> "OpenAICompatibleProvider":
        url = os.environ.get("AIRO_API_URL", "").strip()
        key = os.environ.get("AIRO_API_KEY", "").strip()
        model = os.environ.get("AIRO_MODEL", "").strip()
        if not url or not model:
            raise RuntimeError("configure AIRO_API_URL and AIRO_MODEL; AIRO_API_KEY is required when the provider requires authentication")
        return cls(url, key, model)

    def generate(self, request: ProviderRequest) -> Iterable[ProviderEvent]:
        yield ProviderEvent("start")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": request.system} if request.system else None,
                {"role": "user", "content": request.prompt},
            ],
            "stream": False,
        }
        payload["messages"] = [m for m in payload["messages"] if m is not None]
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request_obj = urllib.request.Request(
            f"{self.base_url}/chat/completions", data=body, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(request_obj, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"model provider returned http {exc.code}: {detail[:1000]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"could not reach model provider: {exc.reason}") from exc

        choices = result.get("choices") or []
        if not choices:
            raise RuntimeError("model provider returned no choices")
        message = choices[0].get("message") or {}
        text = message.get("content")
        if not isinstance(text, str):
            raise RuntimeError("model provider returned an invalid message")
        yield ProviderEvent("text", text)
        yield ProviderEvent("complete")
