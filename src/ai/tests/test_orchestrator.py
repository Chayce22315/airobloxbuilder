from airo_ai.orchestrator import Orchestrator
from airo_ai.providers import EchoProvider

def test_orchestrator_routes_and_uses_model():
    result = Orchestrator(EchoProvider()).run("make a multiplayer mall with zombies")
    assert result.intent == "world"
    assert "orchestrator" in [job.agent for job in result.jobs]
    assert "world" in [job.agent for job in result.jobs]
    assert "offline model response" in result.response
