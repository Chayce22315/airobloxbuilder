from dataclasses import dataclass, field
from .router import Intent

@dataclass
class PlanDraft:
    goal: str
    phases: list[str] = field(default_factory=list)
    agents: list[str] = field(default_factory=list)

def draft_plan(text: str) -> PlanDraft:
    req=text.strip()
    lower=req.lower()
    phases=["foundation","implementation","integration","testing"]
    agents=["orchestrator"]
    if "multiplayer" in lower:
        phases.insert(1,"networking")
        agents.append("networking")
    if any(x in lower for x in ("map","world","level","mall","building","area","environment","zone","city")):
        agents.append("world")
    if any(x in lower for x in ("script","luau","code","function")):
        agents.append("code")
    agents.append("testing")
    return PlanDraft(req,phases,agents)
