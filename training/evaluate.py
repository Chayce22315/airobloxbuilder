import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def evaluate(path: Path) -> dict:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    valid = [r for r in rows if isinstance(r, dict) and r.get("prompt") and r.get("response")]
    duplicates = len(valid) - len({r["prompt"] for r in valid})
    return {"examples": len(rows), "valid": len(valid), "duplicates": duplicates}

def main() -> None:
    for path in sorted((ROOT / "datasets").glob("*.jsonl")):
        print(path.name, evaluate(path))

if __name__ == "__main__":
    main()
