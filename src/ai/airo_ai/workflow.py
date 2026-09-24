from dataclasses import dataclass
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, Future

class WorkKind(str, Enum):
    CHAT = "chat"
    CODE = "code"

@dataclass(frozen=True)
class WorkItem:
    kind: WorkKind
    text: str

@dataclass(frozen=True)
class WorkResult:
    kind: WorkKind
    text: str
    output: str

def classify_work(text: str) -> WorkItem:
    lower = text.lower()
    code_markers = ("write", "create", "add", "implement", "script", "luau", "code", "function")
    kind = WorkKind.CODE if any(marker in lower for marker in code_markers) else WorkKind.CHAT
    return WorkItem(kind, text.strip())

def run_chat(item: WorkItem) -> WorkResult:
    return WorkResult(item.kind, item.text, f"chat response ready for: {item.text}")

def run_code(item: WorkItem) -> WorkResult:
    return WorkResult(item.kind, item.text, f"code task prepared for: {item.text}")

def run_concurrent(items: list[WorkItem]) -> list[WorkResult]:
    handlers = {WorkKind.CHAT: run_chat, WorkKind.CODE: run_code}
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures: list[Future[WorkResult]] = [
            pool.submit(handlers[item.kind], item) for item in items
        ]
        return [future.result() for future in futures]
