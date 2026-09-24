from airo_ai.router import Intent, route_request

def test_plan_intent():
    assert route_request("/plan make a game").intent is Intent.PLAN

def test_world_intent():
    assert route_request("make the mall twice as large").intent is Intent.WORLD
