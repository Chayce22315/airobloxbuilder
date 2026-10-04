import io
import json

from airo_ai.ipc import encode_event, serve
from airo_ai.memory import ProjectMemory
from airo_ai.providers import EchoProvider, ProviderRequest
from airo_ai.tools import ToolRegistry
from airo_ai.trajectory import Trajectory


def test_provider_streams_events():
    events = list(EchoProvider().generate(ProviderRequest("make a mall")))
    assert [event.type for event in events] == ["start", "text", "complete"]


def test_memory_context_is_stable():
    memory = ProjectMemory("mall")
    memory.add_decision("rounds last five minutes")
    memory.add_issue("missing basement path")
    assert "rounds last five minutes" in memory.context()
    assert "missing basement path" in memory.context()


def test_tool_registry_inspects_project(tmp_path):
    (tmp_path / "game.luau").write_text("return true", encoding="utf-8")
    result = ToolRegistry().run("project.inspect", root=str(tmp_path))
    assert result.ok
    assert "game.luau" in result.output


def test_tool_registry_reads_and_writes_project_files(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "game.luau").write_text("return 1", encoding="utf-8")

    read = ToolRegistry().run("project.read", root=str(tmp_path), path="src/game.luau")
    assert read.ok
    assert read.output == "return 1"

    write = ToolRegistry().run(
        "project.write",
        root=str(tmp_path),
        changes=[{
            "path": "src/game.luau",
            "action": "update",
            "content": "return 2",
        }],
    )
    assert write.ok
    assert (tmp_path / "src" / "game.luau").read_text(encoding="utf-8") == "return 2"


def test_tool_registry_rejects_unsafe_write(tmp_path):
    result = ToolRegistry().run(
        "project.write",
        root=str(tmp_path),
        changes=[{
            "path": "../outside.luau",
            "action": "create",
            "content": "return true",
        }],
    )
    assert not result.ok


def test_ipc_emits_json_lines():
    incoming = io.StringIO(json.dumps({"request_id": "7", "text": "hello"}) + "\n")
    outgoing = io.StringIO()
    serve(incoming, outgoing, provider=EchoProvider())
    events = [json.loads(line) for line in outgoing.getvalue().splitlines()]
    assert events[-1]["type"] == "complete"
    assert events[-1]["request_id"] == "7"


def test_trajectory_is_serializable():
    value = Trajectory("make a game", "foundation", "code", "game.luau", "passed", accepted=True)
    assert json.loads(value.to_json())["accepted"] is True
