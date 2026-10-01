from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol
import gc
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
    """Calls any OpenAI-compatible /chat/completions endpoint."""
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


class SpecialistRuntime:
    """Loads a trained QLoRA adapter for one specialist on demand.

    Adapters are discovered from AIRO_ADAPTER_ROOT/<agent>. The base model is
    read from training/model_registry.json, and training_metadata.json is used
    to prevent accidentally pairing an adapter with the wrong base model.
    Only one specialist is kept resident at a time by default, which matters
    on small GPUs such as an 8 GB RTX 5060.
    """

    def __init__(self, registry_path: Path | None = None, adapter_root: Path | None = None) -> None:
        root = Path(__file__).resolve().parents[3]
        self.registry_path = registry_path or root / "training" / "model_registry.json"
        self.adapter_root = adapter_root or Path(
            os.environ.get("AIRO_ADAPTER_ROOT", str(root / "models" / "adapters"))
        )
        self._agent = None
        self._tokenizer = None
        self._model = None

    def _config(self, agent: str) -> dict:
        data = json.loads(self.registry_path.read_text(encoding="utf-8"))
        try:
            return data["models"][agent]
        except KeyError as exc:
            raise RuntimeError(f"no specialist model registered for {agent!r}") from exc

    def adapter_path(self, agent: str) -> Path:
        configured = self._config(agent).get("runtime_adapter_dir")
        if configured:
            return self.adapter_root / configured
        return self.adapter_root / agent

    def available(self, agent: str) -> bool:
        try:
            path = self.adapter_path(agent)
        except RuntimeError:
            return False
        return (path / "adapter_config.json").is_file() and (path / "adapter_model.safetensors").is_file()

    def load(self, agent: str):
        if self._agent == agent and self._model is not None:
            return self._tokenizer, self._model

        if not self.available(agent):
            raise FileNotFoundError(f"trained {agent} adapter not found at {self.adapter_path(agent)}")

        config = self._config(agent)
        base_model = config["model_id"]
        metadata_path = self.adapter_path(agent) / "training_metadata.json"
        if metadata_path.is_file():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            trained_base = metadata.get("base_model")
            if trained_base and trained_base != base_model:
                raise RuntimeError(
                    f"{agent} adapter was trained from {trained_base!r}, "
                    f"but the registry expects {base_model!r}"
                )

        try:
            import torch
            from peft import PeftModel
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        except ImportError as exc:
            raise RuntimeError(
                "specialist adapters require torch, transformers, peft, and accelerate"
            ) from exc

        self.unload()
        tokenizer = AutoTokenizer.from_pretrained(
            str(self.adapter_path(agent)), trust_remote_code=True
        )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        if not torch.cuda.is_available():
            raise RuntimeError("specialist inference requires CUDA; use the normal provider for CPU inference")
        quantization = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        base = AutoModelForCausalLM.from_pretrained(
            base_model,
            quantization_config=quantization,
            device_map={"": 0},
            trust_remote_code=True,
        )
        model = PeftModel.from_pretrained(base, str(self.adapter_path(agent)))
        model.eval()
        self._agent = agent
        self._tokenizer = tokenizer
        self._model = model
        return tokenizer, model

    def unload(self) -> None:
        self._model = None
        self._tokenizer = None
        self._agent = None
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass

    def generate(self, agent: str, request: ProviderRequest) -> Iterable[ProviderEvent]:
        tokenizer, model = self.load(agent)
        try:
            import torch
            prompt = request.prompt
            if request.system:
                prompt = f"{request.system}\n\nuser request:\n{request.prompt}"
            inputs = tokenizer(prompt, return_tensors="pt")
            device = next(model.parameters()).device
            inputs = {key: value.to(device) for key, value in inputs.items()}
            with torch.inference_mode():
                output = model.generate(
                    **inputs,
                    max_new_tokens=int(os.environ.get("AIRO_SPECIALIST_MAX_TOKENS", "1024")),
                    do_sample=False,
                    pad_token_id=tokenizer.pad_token_id,
                )
            generated = output[0][inputs["input_ids"].shape[1]:]
            text = tokenizer.decode(generated, skip_special_tokens=True).strip()
            yield ProviderEvent("start")
            yield ProviderEvent("text", text)
            yield ProviderEvent("complete")
        except Exception as exc:
            raise RuntimeError(f"{agent} specialist generation failed: {exc}") from exc


class SpecialistProvider:
    """Adapter-backed provider with automatic fallback to the normal provider."""

    def __init__(self, fallback: ModelProvider, runtime: SpecialistRuntime | None = None) -> None:
        self.fallback = fallback
        self.runtime = runtime or SpecialistRuntime()

    def generate_for_agent(self, agent: str, request: ProviderRequest) -> Iterable[ProviderEvent]:
        if self.runtime.available(agent):
            yield from self.runtime.generate(agent, request)
        else:
            yield from self.fallback.generate(request)
