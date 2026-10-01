from dataclasses import dataclass
import json
from pathlib import Path
from .luau import ValidationReport, validate_project_full

@dataclass(frozen=True)
class FileChange:
    path: str
    action: str
    content: str = ""

@dataclass(frozen=True)
class ProjectContext:
    root: Path
    files: tuple[str, ...]
    contents: tuple[tuple[str, str], ...] = ()

    @classmethod
    def inspect(cls, root: Path, include_contents: bool = True, max_files: int = 200) -> "ProjectContext":
        root.mkdir(parents=True, exist_ok=True)
        paths = sorted(p for p in root.rglob("*") if p.is_file())[:max_files]
        names = tuple(p.relative_to(root).as_posix() for p in paths)
        if not include_contents:
            return cls(root, names)
        rows = []
        for path in paths:
            if path.suffix.lower() not in {".luau", ".json", ".toml", ".md"}:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            rows.append((path.relative_to(root).as_posix(), content[:12000]))
        return cls(root, names, tuple(rows))

    def prompt(self) -> str:
        listing = "\n".join(self.files) or "(empty project)"
        text = [f"project files:\n{listing}"]
        if self.contents:
            text.append("relevant file contents:\n" + "\n\n".join(f"--- {p} ---\n{c}" for p, c in self.contents))
        return "\n\n".join(text)

def parse_changes(text: str) -> tuple[FileChange, ...]:
    candidates = [text.strip()]
    marker = "```json"
    if marker in text:
        for part in text.split(marker)[1:]:
            if "```" in part:
                candidates.append(part.split("```", 1)[0].strip())
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        rows = payload.get("files") if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            continue
        result = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            path = str(row.get("path", "")).strip().replace("\\", "/")
            action = str(row.get("action", "create")).strip().lower()
            content = row.get("content", "")
            if path and action in {"create", "update", "delete"} and isinstance(content, str):
                result.append(FileChange(path, action, content))
        return tuple(result)
    return ()

def _safe_path(root: Path, relative: str) -> Path:
    target = (root / relative).resolve()
    base = root.resolve()
    if target != base and base not in target.parents:
        raise ValueError(f"unsafe project path: {relative}")
    return target

def validate_changes(root: Path, changes: tuple[FileChange, ...]) -> tuple[str, ...]:
    issues = []
    seen = set()
    for change in changes:
        if change.path in seen:
            issues.append(f"duplicate file change: {change.path}")
        seen.add(change.path)
        if not change.path.startswith(("src/", "assets/", "tests/")):
            issues.append(f"file is outside allowed project roots: {change.path}")
        try:
            target = _safe_path(root, change.path)
        except ValueError as exc:
            issues.append(str(exc))
            continue
        if change.action == "create" and target.exists():
            issues.append(f"create requested for existing file: {change.path}")
        if change.action == "update" and not target.exists():
            issues.append(f"update requested for missing file: {change.path}")
        if change.action in {"create", "update"} and not change.content.strip():
            issues.append(f"empty content for {change.path}")
    return tuple(issues)

def apply_changes(root: Path, changes: tuple[FileChange, ...]) -> None:
    issues = validate_changes(root, changes)
    if issues:
        raise ValueError("\n".join(issues))
    for change in changes:
        target = _safe_path(root, change.path)
        if change.action == "delete":
            if target.exists():
                target.unlink()
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(change.content, encoding="utf-8")

def validate_after_changes(root: Path) -> ValidationReport:
    return validate_project_full(root)
