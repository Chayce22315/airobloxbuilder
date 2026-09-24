from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ModelRequest:
    prompt: str
    system: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str
    finish_reason: str = "stop"
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class AgentRoute:
    agent: str
    reason: str
    priority: int = 0

@dataclass(frozen=True)
class PlanStep:
    id: str
    title: str
    agent: str
    dependencies: tuple[str, ...] = ()

@dataclass(frozen=True)
class Plan:
    request: str
    steps: tuple[PlanStep, ...]

_KEYWORDS = {
    "world": ("map", "world", "mall", "level", "terrain", "building"),
    "code": ("script", "code", "luau", "system", "mechanic"),
    "assets": ("model", "texture", "asset", "skin", "mesh"),
    "animation": ("animation", "rig", "animate"),
    "audio": ("music", "sound", "audio", "sfx"),
    "testing": ("test", "verify", "bug", "error"),
    "repair": ("fix", "repair", "broken", "crash"),
}

def route_request(prompt: str) -> list[AgentRoute]:
    text = prompt.lower()
    routes = [AgentRoute("orchestrator", "every request starts with orchestration", 100)]
    for agent, keywords in _KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            routes.append(AgentRoute(agent, f"matched capability keywords for {agent}", 50))
    return sorted(routes, key=lambda route: route.priority, reverse=True)

def make_plan(request: str) -> Plan:
    request = request.strip()
    steps = [PlanStep("analyze", "analyze the request and current project", "orchestrator")]
    if any(word in request.lower() for word in ("map", "world", "level", "mall")):
        steps.append(PlanStep("build-world", "construct or update requested world content", "world", ("analyze",)))
        implementation_deps = ("analyze", "build-world")
    else:
        implementation_deps = ("analyze",)
    steps.append(PlanStep("implement", "implement required game systems", "code", implementation_deps))
    steps.append(PlanStep("verify", "run tests and inspect generated changes", "testing", ("implement",)))
    return Plan(request=request, steps=tuple(steps))
