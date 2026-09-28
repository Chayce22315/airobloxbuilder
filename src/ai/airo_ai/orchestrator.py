from dataclasses import dataclass, field
from .planner import draft_plan
from .router import route_request
from .providers import ModelProvider, ProviderRequest
from .memory import ProjectMemory

@dataclass(frozen=True)
class AgentJob:
    agent: str
    objective: str
    status: str = "pending"

@dataclass
class OrchestrationResult:
    request: str
    intent: str
    response: str
    jobs: list[AgentJob] = field(default_factory=list)
    plan: object | None = None

class Orchestrator:
    def __init__(self, provider: ModelProvider, project_name: str = "my game") -> None:
        self.provider = provider
        self.memory = ProjectMemory(project_name)

    def run(self, text: str) -> OrchestrationResult:
        request = route_request(text)
        plan = draft_plan(text)
        agents = list(dict.fromkeys(plan.agents))
        jobs = [AgentJob(agent, f"work on: {text}", "queued") for agent in agents]
        system = (
            "you are the lead orchestrator for airobloxbuilder. "
            "coordinate roblox game development agents. "
            "return a useful answer to the user, not a placeholder. "
            "if this is a build request, summarize the plan, agents involved, "
            "and concrete next implementation steps.\n\n"
            + self.memory.context()
        )
        chunks: list[str] = []
        for event in self.provider.generate(ProviderRequest(text, system)):
            if event.type == "text":
                chunks.append(event.text)
        response = "".join(chunks).strip()
        if not response:
            response = "the model returned an empty response."
        return OrchestrationResult(text, request.intent.value, response, jobs, plan)
