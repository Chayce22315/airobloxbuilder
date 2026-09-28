from dataclasses import dataclass, asdict
import json

@dataclass(frozen=True)
class Trajectory:
    request: str
    plan: str
    agent: str
    artifact: str
    test_result: str
    repair: str = ""
    accepted: bool = False

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
