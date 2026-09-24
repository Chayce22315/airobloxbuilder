from airo_ai import make_plan, route_request, Intent

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
    chat = route_request("explain how the zombie round works")
    code = route_request("write the Luau function for the zombie round")
    assert chat.intent == Intent.CHAT
    assert code.intent == Intent.CODE
    assert chat.text != code.text
