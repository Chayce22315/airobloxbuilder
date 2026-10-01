from dataclasses import dataclass, field
from pathlib import Path
from .planner import draft_plan
from .router import route_request
from .providers import ModelProvider, ProviderRequest, SpecialistProvider
from .memory import ProjectMemory
from .project_engine import ProjectContext, FileChange, parse_changes, validate_changes, apply_changes, validate_after_changes

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
    changes: tuple[FileChange, ...] = ()
    validation: object | None = None

class Orchestrator:
    def __init__(self, provider: ModelProvider, project_name: str = "my game", project_root: Path | None = None) -> None:
        self.provider = provider
        self.specialists = SpecialistProvider(provider)
        self.memory = ProjectMemory(project_name)
        self.project_root = Path(project_root) if project_root else None

    def _system(self, agent: str, context: str) -> str:
        base = (
            "you are an airobloxbuilder specialist. work only on the assigned responsibility. "
            "return concrete implementation output, not roleplay. preserve existing project constraints and dependencies.\n\n"
            + self.memory.context()
        )
        if agent == "orchestrator":
            return "you are the lead orchestrator for airobloxbuilder. coordinate roblox game development specialists. summarize the plan and concrete implementation steps.\n\n" + self.memory.context()
        if agent in {"code", "world", "assets", "animation", "audio", "ui", "npc", "networking", "testing", "repair"}:
            base += f"\n\nyour specialist role: {agent}"
            if agent in {"code", "world", "npc", "networking", "ui"}:
                base += """

when you need to modify the project, return JSON only in this exact shape:
{"files":[{"path":"src/ServerScriptService/Example.server.luau","action":"create","content":"..."}]}
use create only for missing files and update only for existing files. never use absolute paths or paths containing .. .
"""
        if context:
            base += "\n\n" + context
        return base

    def _request_changes(self, agent: str, objective: str, system: str) -> tuple[FileChange, ...]:
        chunks = []
        for event in self.specialists.generate_for_agent(agent, ProviderRequest(objective, system)):
            if event.type == "text":
                chunks.append(event.text)
        return parse_changes("".join(chunks))

    def run(self, text: str) -> OrchestrationResult:
        request = route_request(text)
        plan = draft_plan(text)
        agents = list(dict.fromkeys(plan.agents))
        project = ProjectContext.inspect(self.project_root) if self.project_root else None
        context = project.prompt() if project else ""
        jobs = []
        outputs = []
        changes: tuple[FileChange, ...] = ()
        validation = None

        for agent in agents:
            objective = f"work on the {agent} specialist portion of this request: {text}"
            adapter_active = self.specialists.runtime.available(agent)
            provider_name = f"qlora:{agent}" if adapter_active else "fallback"
            jobs.append(AgentJob(agent, objective, "queued", provider_name))
            system = self._system(agent, context)
            result_chunks = []
            for event in self.specialists.generate_for_agent(agent, ProviderRequest(objective, system)):
                if event.type == "text":
                    result_chunks.append(event.text)
            result = "".join(result_chunks).strip()
            if result:
                outputs.append(f"[{agent}]\n{result}")
            if agent == "code" and project:
                changes = parse_changes(result)

        if project and changes:
            change_issues = validate_changes(project.root, changes)
            if change_issues:
                outputs.append("[project]\nrejected unsafe or inconsistent changes:\n" + "\n".join(change_issues))
            else:
                apply_changes(project.root, changes)
                validation = validate_after_changes(project.root)
                if not validation.ok:
                    repair_system = self._system("repair", project.prompt())
                    repair_request = (
                        "repair the generated Roblox project. validation failed:\n"
                        + validation.summary
                        + "\nreturn JSON file changes only. use action update for existing files and create for new files."
                    )
                    repair_changes = self._request_changes("repair", repair_request, repair_system)
                    repair_issues = validate_changes(project.root, repair_changes)
                    if not repair_issues and repair_changes:
                        apply_changes(project.root, repair_changes)
                        changes = changes + repair_changes
                        validation = validate_after_changes(project.root)
                    else:
                        outputs.append("[repair]\nno safe repair changes were produced")
                outputs.append("[testing]\n" + validation.summary)

        response = "\n\n".join(outputs).strip() or "the model returned an empty response."
        return OrchestrationResult(text, request.intent.value, response, jobs, plan, changes, validation)
