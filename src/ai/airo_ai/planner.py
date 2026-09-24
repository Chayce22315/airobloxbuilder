from dataclasses import dataclass, field
from .router import Intent

@dataclass
class PlanDraft:
    goal: str
    phases: list[str] = field(default_factory=list)
    agents: list[str] = field(default_factory=list)

def draft_plan(text: str) -> PlanDraft:
    req=text.strip()
    phases=["foundation","implementation","integration","testing"]
    agents=["orchestrator"]
    if "multiplayer" in req.lower(): phases.insert(1,"networking"); agents.append("networking")
    if any(x in req.lower() for x in ("map","world","level")): agents.append("world")
    if any(x in req.lower() for x in ("script","luau","code")): agents.append("code")
    agents.append("testing")
    return PlanDraft(req,phases,agents)
