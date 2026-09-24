from airo_ai.planner import make_plan
from airo_ai.router import route_request

def test_routes_orchestrator_first():
    routes = route_request("make a mall with a zombie system")
    assert routes[0].agent == "orchestrator"
    assert {route.agent for route in routes} >= {"world", "code"}

def test_plan_has_verification():
    plan = make_plan("make a multiplayer mall")
    assert plan.steps[-1].id == "verify"
    assert "build-world" in {step.id for step in plan.steps}
