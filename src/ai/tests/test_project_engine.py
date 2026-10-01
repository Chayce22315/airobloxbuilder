import json
from pathlib import Path

from airo_ai.luau import validate_text, validate_project
from airo_ai.project_engine import FileChange, ProjectContext, apply_changes, parse_changes, validate_changes

def test_parse_structured_file_changes():
    text = '{"files":[{"path":"src/ServerScriptService/Game.server.luau","action":"create","content":"return true"}]}'
    changes = parse_changes(text)
    assert len(changes) == 1
    assert changes[0].path.endswith("Game.server.luau")

def test_parse_fenced_json_changes():
    changes = parse_changes('```json\n{"files":[{"path":"src/a.luau","action":"create","content":"return true"}]}\n```')
    assert changes[0].action == "create"

def test_project_context_includes_luau_contents(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.luau").write_text("return true", encoding="utf-8")
    context = ProjectContext.inspect(tmp_path)
    assert "src/a.luau" in context.files
    assert "return true" in context.prompt()

def test_change_paths_are_sandboxed(tmp_path):
    issues = validate_changes(tmp_path, (FileChange("../escape.luau", "create", "return true"),))
    assert issues

def test_apply_and_validate_generated_luau(tmp_path):
    changes = (FileChange("src/ServerScriptService/Game.server.luau", "create", "local x = 1\nreturn x"),)
    apply_changes(tmp_path, changes)
    report = validate_project(tmp_path)
    assert report.ok

def test_luau_validator_catches_unclosed_block():
    issues = validate_text("bad.luau", "local function nope()\n    return true")
    assert issues

def test_luau_validator_catches_unexpected_end():
    issues = validate_text("bad.luau", "return true\nend")
    assert issues


def test_ensure_project_layout_creates_rojo_manifest(tmp_path):
    from airo_ai.project_engine import ensure_project_layout
    ensure_project_layout(tmp_path, "zombie mall")
    manifest = json.loads((tmp_path / "project.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "zombie mall"
    assert (tmp_path / "src" / "ServerScriptService").is_dir()
