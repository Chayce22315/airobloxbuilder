import json
import sys
from pathlib import Path
from typing import TextIO
from .providers import OpenAICompatibleProvider, ProviderRequest
from .orchestrator import Orchestrator

SYSTEM_PROMPT = """you are airobloxbuilder, a roblox game development ai. you help build games with luau, worlds, assets, ui, gameplay, testing, repair, and project tools."""

def encode_event(event_type: str, request_id: str, message: str, **extra) -> str:
    payload = {"type": event_type, "request_id": request_id, "message": message, **extra}
    return json.dumps(payload, ensure_ascii=False)

def serve(reader: TextIO = sys.stdin, writer: TextIO = sys.stdout, provider=None) -> None:
    if provider is None:
        provider = OpenAICompatibleProvider.from_environment()
    for line in reader:
        if not line.strip():
            continue
        request = json.loads(line)
        request_id = str(request.get("request_id", ""))
        text = str(request.get("text", "")).strip()
        project_root_value = str(request.get("project_root", "")).strip()
        project_root = Path(project_root_value) if project_root_value else None
        if not text:
            writer.write(encode_event("error", request_id, "empty request") + "\n")
            writer.flush()
            continue
        try:
            writer.write(encode_event("progress", request_id, "orchestrator received request") + "\n")
            writer.flush()
            orchestrator = Orchestrator(provider, project_root=project_root)
            result = orchestrator.run(text)
            writer.write(encode_event(
                "route", request_id, f"routed to: {', '.join(job.agent for job in result.jobs)}",
                agents=[job.agent for job in result.jobs], intent=result.intent
            ) + "\n")
            if result.changes:
                writer.write(encode_event(
                    "files", request_id, f"applied {len(result.changes)} project changes",
                    changes=[{"path": c.path, "action": c.action} for c in result.changes]
                ) + "\n")
            if result.validation is not None:
                writer.write(encode_event(
                    "validation", request_id, result.validation.summary, ok=result.validation.ok
                ) + "\n")
            writer.write(encode_event("text", request_id, result.response) + "\n")
            writer.write(encode_event("complete", request_id, "orchestration complete") + "\n")
            writer.flush()
        except Exception as exc:
            writer.write(encode_event("error", request_id, str(exc)) + "\n")
            writer.flush()
