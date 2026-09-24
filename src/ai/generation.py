from dataclasses import dataclass
from .model_runtime import GenerationRequest, GenerationResult, ModelRegistry
from .airo_ai import Plan

@dataclass(frozen=True)
class GenerationJob:
    id: str
    plan: Plan
    target: str = "roblox"

def build_generation_requests(job: GenerationJob) -> list[GenerationRequest]:
    requests: list[GenerationRequest] = []
    for step in job.plan.steps:
        requests.append(GenerationRequest(
            prompt=f"implement task '{step.title}' for a roblox project",
            system="produce deterministic, reviewable changes; do not claim tools you do not have",
            metadata={"job_id": job.id, "step_id": step.id, "agent": step.agent},
        ))
    return requests

def generate_job(job: GenerationJob, registry: ModelRegistry, provider: str) -> list[GenerationResult]:
    model = registry.get(provider)
    return [model.generate(request) for request in build_generation_requests(job)]
