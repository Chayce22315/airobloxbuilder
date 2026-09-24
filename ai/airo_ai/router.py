from dataclasses import dataclass
@dataclass(frozen=True)
class AiRequest: text:str; project_summary:str=""
@dataclass(frozen=True)
class AiRoute: kind:str; agents:tuple[str,...]
def route_request(request:AiRequest)->AiRoute:
    text=request.text.strip().lower()
    if text.startswith("/plan"): return AiRoute("plan",("orchestrator","planner"))
    if text=="/test": return AiRoute("test",("testing",))
    if text=="/fix": return AiRoute("fix",("repair","testing"))
    return AiRoute("build",("orchestrator","code","world"))