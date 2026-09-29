from dataclasses import dataclass, field
from .planner import draft_plan
from .router import route_request
from .providers import ModelProvider, ProviderRequest, SpecialistProvider
from .memory import ProjectMemory

@dataclass(frozen=True)
class AgentJob:
    agent: str
    objective: str
    status: str = "pending"
    provider: str = "fallback"

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
        self.specialists = SpecialistProvider(provider)
        self.memory = ProjectMemory(project_name)

    def run(self, text: str) -> OrchestrationResult:
        request = route_request(text)
        plan = draft_plan(text)
        agents = list(dict.fromkeys(plan.agents))

        jobs: list[AgentJob] = []
        outputs: list[str] = []

        base_system = (
            "you are an airobloxbuilder specialist. "
            "work only on the assigned responsibility. "
            "return concrete implementation output, not roleplay. "
            "preserve existing project constraints and dependencies.\n\n"
            + self.memory.context()
        )

        for agent in agents:
            objective = f"work on the {agent} specialist portion of this request: {text}"
            adapter_active = agent not in ("orchestrator", "networking") and self.specialists.runtime.available(agent)
            provider_name = f"qlora:{agent}" if adapter_active else "fallback"
            jobs.append(AgentJob(agent, objective, "queued", provider_name))

            if agent == "orchestrator":
                system = (
                    "you are the lead orchestrator for airobloxbuilder. "
                    "coordinate roblox game development specialists. "
                    "summarize the plan and concrete implementation steps.\n\n"
                    + self.memory.context()
                )
            else:
                system = base_system + f"\n\nyour specialist role: {agent}"

            chunks: list[str] = []
            for event in self.specialists.generate_for_agent(
                agent,
                ProviderRequest(objective, system),
            ):
                if event.type == "text":
                    chunks.append(event.text)
            result = "".join(chunks).strip()
            if result:
                outputs.append(f"[{agent}]\n{result}")

        response = "\n\n".join(outputs).strip()
        if not response:
            response = "the model returned an empty response."
        return OrchestrationResult(text, request.intent.value, response, jobs, plan)
