from dataclasses import dataclass
from enum import Enum

class Intent(str, Enum):
    PLAN="plan"
    CODE="code"
    WORLD="world"
    ASSET="asset"
    TEST="test"
    FIX="fix"
    CHAT="chat"

@dataclass(frozen=True)
class ModelRequest:
    text: str
    intent: Intent
    needs_tools: bool = True

def route_request(text: str) -> ModelRequest:
    value=text.strip()
    lower=value.lower()
    if lower.startswith("/plan"):
        intent=Intent.PLAN
    elif lower.startswith("/test"):
        intent=Intent.TEST
    elif lower.startswith("/fix"):
        intent=Intent.FIX
    elif any(x in lower for x in ("map","world","level","spawn","mall","building","area","environment","zone","city")):
        intent=Intent.WORLD
    elif any(x in lower for x in ("script","luau","code","function")):
        intent=Intent.CODE
    elif any(x in lower for x in ("model","texture","asset","character")):
        intent=Intent.ASSET
    else:
        intent=Intent.CHAT
    return ModelRequest(value,intent)
