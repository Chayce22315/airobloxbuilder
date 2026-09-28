import json
import sys
from typing import TextIO

def encode_event(event_type: str, request_id: str, message: str, **extra) -> str:
    payload = {"type": event_type, "request_id": request_id, "message": message, **extra}
    return json.dumps(payload, ensure_ascii=False)

def serve(reader: TextIO = sys.stdin, writer: TextIO = sys.stdout) -> None:
    for line in reader:
        if not line.strip():
            continue
        request = json.loads(line)
        request_id = str(request.get("request_id", ""))
        text = str(request.get("text", "")).strip()
        writer.write(encode_event("progress", request_id, f"received: {text}") + "\n")
        writer.write(encode_event("complete", request_id, "ai runtime ready") + "\n")
        writer.flush()
