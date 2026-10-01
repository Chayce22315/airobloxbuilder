from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class FileChange:
    path: str
    action: str
    content: str = ""
