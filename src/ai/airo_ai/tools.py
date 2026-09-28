from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ToolResult:
    ok: bool
    output: str

class ToolRegistry:
    def __init__(self) -> None:
        self._tools = {"project.inspect": self.inspect}

    def names(self) -> tuple[str, ...]:
        return tuple(self._tools)

    def run(self, name: str, **kwargs) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(False, f"unknown tool: {name}")
        return tool(**kwargs)

    def inspect(self, root: str = ".") -> ToolResult:
        path = Path(root)
        if not path.exists():
            return ToolResult(False, f"project path does not exist: {root}")
        entries = [p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()][:200]
        return ToolResult(True, "\n".join(entries) or "(empty project)")
