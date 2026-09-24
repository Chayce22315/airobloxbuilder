from dataclasses import dataclass
from typing import Mapping, Sequence
import json
from urllib.request import Request, urlopen

@dataclass(frozen=True)
class ModelConfig:
    endpoint: str
    model: str
    api_key: str | None = None
    timeout: float = 60.0

class ModelError(RuntimeError):
    pass

def chat(config: ModelConfig, messages: Sequence[Mapping[str, str]]) -> str:
    payload=json.dumps({"model":config.model,"messages":list(messages)}).encode()
    headers={"content-type":"application/json"}
    if config.api_key: headers["authorization"]=f"Bearer {config.api_key}"
    try:
        req=Request(config.endpoint.rstrip("/")+"/chat/completions",data=payload,headers=headers,method="POST")
        with urlopen(req,timeout=config.timeout) as response:
            body=json.loads(response.read())
        return body["choices"][0]["message"]["content"]
    except Exception as exc:
        raise ModelError(f"model request failed: {exc}") from exc
