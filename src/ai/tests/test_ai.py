from airo_ai import make_plan, route_request, Intent
from airo_ai.workflow import WorkKind, classify_work, run_concurrent

def test_routes_code_and_world():
    request = route_request("make a mall with a zombie system")
    assert request.intent in {Intent.WORLD, Intent.CODE}

def test_plan_has_verification_and_agents():
    plan = make_plan("make a multiplayer mall with scripts")
    assert plan.phases[-1] == "testing"
    assert "orchestrator" in plan.agents
    assert "networking" in plan.agents
    assert "world" in plan.agents
    assert "code" in plan.agents

def test_chat_and_code_can_coexist():
    chat = classify_work("explain how the zombie round works")
    code = classify_work("write the Luau function for the zombie round")
    assert chat.kind == WorkKind.CHAT
    assert code.kind == WorkKind.CODE

def test_chat_and_code_run_concurrently():
    results = run_concurrent([
        classify_work("explain the zombie round"),
        classify_work("write the Luau round function"),
    ])
    assert {result.kind for result in results} == {WorkKind.CHAT, WorkKind.CODE}
    assert all(result.output for result in results)
