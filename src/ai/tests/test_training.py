import json
from pathlib import Path

from airo_ai.orchestrator import Orchestrator
from airo_ai.providers import EchoProvider, SpecialistProvider, SpecialistRuntime


def test_training_datasets_have_multiple_real_examples():
    root = Path(__file__).parents[3] / "training" / "datasets"
    for path in root.glob("*.jsonl"):
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert len(rows) >= 5
        assert all(row["prompt"] != "example code task" for row in rows)


def test_trajectory_schema_exists():
    path = Path(__file__).parents[3] / "training" / "trajectory_schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert schema["version"] == 1
    assert schema["privacy"]["private_projects_default"] is False


def test_specialist_runtime_maps_each_agent_to_its_adapter_directory(tmp_path):
    registry = {
        "models": {
            "code": {"model_id": "base/code", "runtime_adapter_dir": "code"},
            "testing": {"model_id": "base/testing", "runtime_adapter_dir": "testing"},
        }
    }
    registry_path = tmp_path / "model_registry.json"
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    runtime = SpecialistRuntime(registry_path=registry_path, adapter_root=tmp_path / "adapters")
    assert runtime.adapter_path("code") == tmp_path / "adapters" / "code"
    assert runtime.adapter_path("testing") == tmp_path / "adapters" / "testing"
    assert not runtime.available("code")


def test_specialist_provider_falls_back_when_adapter_is_missing():
    provider = SpecialistProvider(EchoProvider())
    events = list(provider.generate_for_agent("code", type("Request", (), {"prompt": "hello", "system": ""})()))
    assert any(event.type == "text" and "offline model response" in event.text for event in events)


def test_orchestrator_routes_and_uses_model():
    result = Orchestrator(EchoProvider()).run("make a multiplayer mall with zombies")
    assert result.intent == "world"
    assert "orchestrator" in [job.agent for job in result.jobs]
    assert "world" in [job.agent for job in result.jobs]
    assert "offline model response" in result.response
