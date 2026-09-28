import json
import sys
from typing import TextIO
from .providers import OpenAICompatibleProvider, ProviderRequest

SYSTEM_PROMPT = """you are airobloxbuilder, a roblox game development ai.
you help plan and build roblox games using luau, world design, assets, ui, gameplay, testing, repair, and project tools.
be practical and concise. when the user asks to build something, explain the intended implementation and identify files or systems that should change.
"""

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
        if not text:
            writer.write(encode_event("error", request_id, "empty request") + "\n")
            writer.flush()
            continue
        try:
            for event in provider.generate(ProviderRequest(text, SYSTEM_PROMPT)):
                if event.type == "start":
                    writer.write(encode_event("progress", request_id, "model is thinking") + "\n")
                elif event.type == "text":
                    writer.write(encode_event("text", request_id, event.text) + "\n")
                elif event.type == "complete":
                    writer.write(encode_event("complete", request_id, "response complete") + "\n")
                writer.flush()
        except Exception as exc:
            writer.write(encode_event("error", request_id, str(exc)) + "\n")
            writer.flush()
