import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES = {
    "code": [
        ("write a server-side luau function for {feature}", "implement {feature} on the server and validate inputs before changing state"),
        ("debug a luau system where {problem}", "inspect the failing reference, make the smallest safe repair, and add regression coverage"),
    ],
    "gameplay": [
        ("design a gameplay loop for {feature}", "define states, player actions, win/loss conditions, progression, and verification cases"),
        ("add {feature} to an existing game", "integrate the feature with existing systems, preserve compatible behavior, and test affected dependencies"),
    ],
    "world": [
        ("build a roblox area for {feature}", "create readable routes, safe spawn space, gameplay landmarks, and stable hierarchy names"),
        ("expand an existing area with {feature}", "inspect the current layout, extend it without unnecessary replacement, then update dependent paths"),
    ],
    "testing": [
        ("test a system involving {feature}", "cover normal behavior, invalid input, multiplayer state, cleanup, and regression cases"),
        ("investigate an intermittent failure involving {feature}", "capture reproduction conditions, isolate timing or shared-state causes, then verify the repair"),
    ],
}
FEATURES = ["a zombie round", "a mall basement", "a multiplayer shop", "a boss fight", "a save system"]

def generate(agent: str, output: Path) -> int:
    rows = [{"prompt": p.format(feature=f), "response": r.format(feature=f)}
            for p, r in TEMPLATES[agent] for f in FEATURES]
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)

def main() -> None:
    datasets = ROOT / "datasets"
    total = 0
    for agent in TEMPLATES:
        total += generate(agent, datasets / f"{agent}.jsonl")
    print(f"generated {total} synthetic training examples")

if __name__ == "__main__":
    main()
