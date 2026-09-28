import json
import sys
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
    orchestrator = Orchestrator(provider)
    for line in reader:
        if not line.strip():
            continue
        request = json.loads(line)
        request_id = str(request.get("request_id", ""))
        text = str(request.get("text", "")).strip()
        if not text:
            writer.write(encode_event("error", request_id, "empty request") + "\n")
            writer.flush()
            continue
        try:
            writer.write(encode_event("progress", request_id, "orchestrator received request") + "\n")
            writer.flush()
            result = orchestrator.run(text)
            writer.write(encode_event("route", request_id, f"routed to: {', '.join(job.agent for job in result.jobs)}", agents=[job.agent for job in result.jobs], intent=result.intent) + "\n")
            writer.flush()
            writer.write(encode_event("text", request_id, result.response) + "\n")
            writer.write(encode_event("complete", request_id, "orchestration complete") + "\n")
            writer.flush()
        except Exception as exc:
            writer.write(encode_event("error", request_id, str(exc)) + "\n")
            writer.flush()
