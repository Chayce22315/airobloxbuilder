import json
from pathlib import Path

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
