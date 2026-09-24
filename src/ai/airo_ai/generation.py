from dataclasses import dataclass
from .models import ModelConfig, chat

@dataclass(frozen=True)
class GenerationRequest:
    instruction: str
    context: str = ""
    output_kind: str = "luau"

def build_messages(request: GenerationRequest) -> list[dict[str,str]]:
    system=(
        "you are the generation layer for airobloxbuilder. "
        "produce only the requested artifact, respect existing project context, "
        "and never invent tool results."
    )
    user=f"output kind: {request.output_kind}\ninstruction: {request.instruction}\ncontext:\n{request.context}"
    return [{"role":"system","content":system},{"role":"user","content":user}]

def generate(config: ModelConfig, request: GenerationRequest) -> str:
    return chat(config,build_messages(request))
