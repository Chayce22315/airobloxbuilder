from dataclasses import dataclass
import os
import re
import shutil
import subprocess
from pathlib import Path

@dataclass(frozen=True)
class LuauIssue:
    path: str
    message: str
    line: int = 0

@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    issues: tuple[LuauIssue, ...] = ()

    @property
    def summary(self) -> str:
        if self.ok:
            return "luau validation passed"
        return "\n".join(f"{i.path}:{i.line}: {i.message}" for i in self.issues)

def _clean(line: str) -> str:
    line = re.sub(r"--.*$", "", line)
    line = re.sub(r'"(?:\\.|[^"\\])*"', '""', line)
    line = re.sub(r"'(?:\\.|[^'\\])*'", "''", line)
    return line

def validate_text(path: str, text: str) -> list[LuauIssue]:
    issues = []
    blocks = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = _clean(raw)
        for _ in re.findall(r"\b(function|if|for|while)\b", line):
            blocks.append(number)
        for _ in re.findall(r"\brepeat\b", line):
            blocks.append(-number)
        for _ in re.findall(r"\bend\b", line):
            if not blocks:
                issues.append(LuauIssue(path, "unexpected 'end'", number))
            else:
                blocks.pop()
        for _ in re.findall(r"\buntil\b", line):
            idx = next((i for i in range(len(blocks)-1, -1, -1) if blocks[i] < 0), None)
            if idx is None:
                issues.append(LuauIssue(path, "unexpected 'until'", number))
            else:
                blocks.pop(idx)
        for opener, closer in (("(", ")"), ("{", "}"), ("[", "]")):
            depth = 0
            for char in line:
                if char == opener:
                    depth += 1
                elif char == closer:
                    depth -= 1
                if depth < 0:
                    issues.append(LuauIssue(path, f"unexpected '{closer}'", number))
                    break
    for block in blocks:
        issues.append(LuauIssue(path, "unclosed block", abs(block)))
    return issues

def validate_project(root: Path) -> ValidationReport:
    issues = []
    if not root.exists():
        return ValidationReport(False, (LuauIssue(".", f"project path does not exist: {root}"),))
    for path in sorted(root.rglob("*.luau")):
        rel = path.relative_to(root).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(LuauIssue(rel, "file is not valid UTF-8"))
            continue
        issues.extend(validate_text(rel, content))
    return ValidationReport(not issues, tuple(issues))

def validate_with_luau_cli(root: Path) -> ValidationReport | None:
    binary = os.environ.get("AIRO_LUAU_BIN") or shutil.which("luau-analyze")
    if not binary:
        return None
    proc = subprocess.run([binary, str(root)], capture_output=True, text=True, timeout=60)
    if proc.returncode == 0:
        return ValidationReport(True)
    detail = (proc.stderr or proc.stdout).strip() or "Luau analyzer failed"
    return ValidationReport(False, (LuauIssue(".", detail),))

def validate_project_full(root: Path) -> ValidationReport:
    static = validate_project(root)
    if not static.ok:
        return static
    return validate_with_luau_cli(root) or static
