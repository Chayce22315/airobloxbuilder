import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "agents.json").read_text(encoding="utf-8"))

for agent in manifest["agents"]:
    path = ROOT / "datasets" / f"{agent}.jsonl"
    if path.exists():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            row = json.loads(line)
            assert row.get("prompt") and row.get("response"), f"{path}:{number}"
print(f"validated {len(manifest['agents'])} agent definitions")
