from dataclasses import dataclass
from pathlib import Path

from .project_engine import (
    FileChange,
    ProjectContext,
    apply_changes,
    validate_after_changes,
    validate_changes,
)


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    output: str


class ToolRegistry:
    """Small, deterministic tools the model can use against the active project."""

    def __init__(self) -> None:
        self._tools = {
            "project.inspect": self.inspect,
            "project.read": self.read,
            "project.write": self.write,
            "project.validate": self.validate,
        }

    def names(self) -> tuple[str, ...]:
        return tuple(self._tools)

    def run(self, name: str, **kwargs) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(False, f"unknown tool: {name}")
        try:
            return tool(**kwargs)
        except (OSError, ValueError) as exc:
            return ToolResult(False, str(exc))

    def inspect(self, root: str = ".") -> ToolResult:
        path = Path(root)
        if not path.exists():
            return ToolResult(False, f"project path does not exist: {root}")
        entries = [p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()][:200]
        return ToolResult(True, "\n".join(entries) or "(empty project)")

    def read(self, root: str = ".", path: str = "") -> ToolResult:
        project = ProjectContext.inspect(Path(root), include_contents=False)
        target = (project.root / path).resolve()
        base = project.root.resolve()
        if target != base and base not in target.parents:
            return ToolResult(False, f"unsafe project path: {path}")
        if not target.is_file():
            return ToolResult(False, f"project file does not exist: {path}")
        return ToolResult(True, target.read_text(encoding="utf-8"))

    def write(self, root: str = ".", changes: list[dict] | None = None) -> ToolResult:
        if not isinstance(changes, list) or not changes:
            return ToolResult(False, "project.write requires a non-empty changes list")
        parsed = []
        for row in changes:
            if not isinstance(row, dict):
                return ToolResult(False, "each project change must be an object")
            path = str(row.get("path", "")).strip().replace("\\", "/")
            action = str(row.get("action", "create")).strip().lower()
            content = row.get("content", "")
            if not path or action not in {"create", "update", "delete"} or not isinstance(content, str):
                return ToolResult(False, f"invalid project change: {row!r}")
            parsed.append(FileChange(path, action, content))

        project_root = Path(root)
        issues = validate_changes(project_root, tuple(parsed))
        if issues:
            return ToolResult(False, "\n".join(issues))
        apply_changes(project_root, tuple(parsed))
        return ToolResult(True, f"applied {len(parsed)} project change(s)")

    def validate(self, root: str = ".") -> ToolResult:
        path = Path(root)
        if not path.exists():
            return ToolResult(False, f"project path does not exist: {root}")
        report = validate_after_changes(path)
        return ToolResult(report.ok, report.summary)
