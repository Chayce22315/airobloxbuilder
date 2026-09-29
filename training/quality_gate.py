from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = ("prompt", "response", "agent", "scenario", "quality")
RESPONSE_MARKERS = ("plan:", "artifact:", "test_result:", "accepted:")
FORBIDDEN = ("lorem ipsum", "todo", "tbd", "fill in the blank", "{{", "}}")

def validate(path: Path, expected_agent: str | None = None) -> dict:
    seen = set()
    errors = []
    rows = structured = artifact_aware = test_aware = 0

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        rows += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{line_no}: invalid json: {exc}")
            continue

        missing = [key for key in REQUIRED if not row.get(key)]
        if missing:
            errors.append(f"{line_no}: missing {missing}")
            continue
        if expected_agent and row["agent"] != expected_agent:
            errors.append(f"{line_no}: expected agent {expected_agent!r}, got {row['agent']!r}")

        prompt = row["prompt"].strip().lower()
        response = row["response"].strip().lower()
        if prompt in seen:
            errors.append(f"{line_no}: duplicate prompt")
        seen.add(prompt)

        if any(token in prompt or token in response for token in FORBIDDEN):
            errors.append(f"{line_no}: placeholder/low-quality token detected")

        if all(marker in response for marker in RESPONSE_MARKERS):
            structured += 1
        if row["quality"].get("artifact_aware") and "artifact:" in response:
            artifact_aware += 1
        if row["quality"].get("test_aware") and "test_result:" in response:
            test_aware += 1

        if row["quality"].get("private_data"):
            errors.append(f"{line_no}: private_data must be false")
        if not row["quality"].get("permitted_data"):
            errors.append(f"{line_no}: permitted_data must be true")

    if rows == 0:
        errors.append("dataset is empty")

    report = {
        "path": str(path),
        "examples": rows,
        "unique_prompts": len(seen),
        "structured_trajectories": structured,
        "artifact_aware": artifact_aware,
        "test_aware": test_aware,
        "errors": errors,
    }
    if errors:
        raise SystemExit(json.dumps(report, indent=2))
    return report

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--agent")
    args = parser.parse_args()
    print(json.dumps({"datasets": [validate(p, args.agent) for p in args.paths]}, indent=2))

if __name__ == "__main__":
    main()
