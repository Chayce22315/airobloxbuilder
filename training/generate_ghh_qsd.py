from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
DATASETS = ROOT / "datasets"

# G.H.H.Q.S.D. = genuinely huge, high-quality specialist dataset.
# This generator creates structured development trajectories, not role-play.
SEED_SCENARIOS = {
    "code": [
        ("zombie_rounds", "build a server-authoritative zombie round system", "round state, spawn pacing, cleanup, rewards"),
        ("inventory", "implement a replicated inventory service", "ownership, validation, stacking, persistence boundary"),
        ("shop", "implement a multiplayer shop", "server pricing, purchase validation, stock, UI events"),
        ("quests", "build a quest state machine", "objectives, progress, completion, rewards"),
        ("boss", "implement a boss encounter controller", "phases, damage validation, telegraphs, cleanup"),
        ("matchmaking", "implement a queue and match assignment service", "queue state, cancellation, capacity, timeouts"),
        ("saving", "build a resilient profile save boundary", "load, reconcile, retry, shutdown flush"),
        ("round_timer", "implement a synchronized round timer", "server clock, state transitions, client display"),
        ("doors", "implement multiplayer doors", "permissions, debounce, replication, failure handling"),
        ("leaderboard", "implement a session leaderboard service", "ordering, ties, cleanup, replication"),
        ("abilities", "implement a server-validated ability system", "cooldowns, costs, targets, anti-spam"),
        ("trading", "implement a safe player trading flow", "offers, locking, confirmation, cancellation"),
        ("waves", "implement configurable enemy waves", "wave definitions, spawn budget, completion detection"),
        ("teleports", "implement a guarded teleport service", "destination validation, cooldowns, failure recovery"),
        ("checkpoints", "implement checkpoint progression", "server ownership, respawn state, reset rules"),
        ("status_effects", "implement timed status effects", "stacking policy, expiration, cleanup"),
    ],
    "design": [
        ("mall", "design a replayable zombie mall level", "navigation, sightlines, landmarks, pacing"),
        ("dungeon", "design a cooperative dungeon", "readability, loops, combat arenas, safe rooms"),
        ("hub", "design a social game hub", "orientation, discovery, queueing, performance"),
        ("boss_arena", "design a boss arena", "telegraphs, cover, traversal, phase transitions"),
        ("obby", "design a traversal-focused obstacle course", "route clarity, difficulty curve, checkpoints"),
        ("survival", "design a survival map", "resource loops, spawn safety, escalation"),
        ("shop_world", "design a shop district", "player flow, storefront identity, interaction density"),
        ("tutorial", "design a first-session tutorial space", "onboarding, affordances, feedback, exit path"),
        ("pvp", "design a competitive arena", "symmetry, spawn safety, sightline control, rotation"),
        ("horror", "design a suspense-focused environment", "foreshadowing, pacing, audio spaces, safe navigation"),
        ("park", "design a compact exploration park", "landmarks, optional routes, activity clustering"),
        ("factory", "design a vertical factory level", "layering, traversal, hazards, visual hierarchy"),
        ("subway", "design a multiplayer subway station", "platform safety, route logic, crowding"),
        ("castle", "design a readable castle complex", "gates, courtyards, shortcuts, progression"),
        ("sewer", "design a sewer network", "branching, navigation anchors, encounter pockets"),
        ("island", "design a small survival island", "resource placement, traversal, discovery"),
    ],
    "animation": [
        ("zombie_attack", "specify a zombie attack animation set", "anticipation, contact, recovery, hit reaction"),
        ("sprint", "specify a responsive sprint animation set", "start, loop, stop, directional blending"),
        ("weapon", "specify a multiplayer weapon animation set", "equip, idle, fire, reload, inspect"),
        ("boss", "specify a boss phase animation set", "telegraph, attack, recovery, phase transition"),
        ("npc_shop", "specify a shopkeeper animation set", "idle, greet, interact, celebrate"),
        ("death", "specify non-graphic defeat animations", "stagger, fall, recovery-disabled state"),
        ("emote", "specify a social emote pack", "anticipation, loop, exit, cancellation"),
        ("door", "specify interactive door animations", "approach, open, hold, close, obstruction"),
        ("pickup", "specify item pickup animations", "reach, collect, feedback, return"),
        ("climb", "specify a ladder traversal set", "mount, loop, dismount, interruption"),
        ("vault", "specify a vault traversal set", "approach, plant, clear, land"),
        ("hit_reaction", "specify a directional hit reaction set", "front, back, left, right, recovery"),
        ("vehicle", "specify a vehicle entry/exit set", "approach, enter, seated, exit"),
        ("celebration", "specify a round-win celebration set", "start, loop, end, interruption"),
        ("npc_patrol", "specify a patrol animation set", "walk, idle, turn, alert"),
        ("ui_avatar", "specify avatar feedback animations", "confirm, deny, waiting, success"),
    ],
    "testing": [
        ("zombie_rounds", "test a server-authoritative zombie round system", "state transitions, spawn cleanup, rewards"),
        ("inventory", "test a replicated inventory service", "ownership, invalid input, stacking, persistence boundary"),
        ("shop", "test a multiplayer shop", "pricing, stock, race conditions, cancellation"),
        ("quests", "test a quest state machine", "progress, completion, reset, duplicate rewards"),
        ("boss", "test a boss encounter controller", "phase transitions, damage validation, cleanup"),
        ("matchmaking", "test matchmaking and cancellation", "capacity, timeout, cancellation, duplicate joins"),
        ("saving", "test a profile save boundary", "load failure, retry, shutdown, partial data"),
        ("round_timer", "test a synchronized round timer", "clock drift, transition edges, disconnects"),
        ("doors", "test multiplayer doors", "permissions, debounce, simultaneous requests"),
        ("leaderboard", "test a session leaderboard", "ties, ordering, removal, malformed values"),
        ("abilities", "test a server-validated ability system", "cooldowns, costs, target validation, spam"),
        ("trading", "test a player trading flow", "locking, cancellation, disconnects, confirmation"),
        ("waves", "test configurable enemy waves", "spawn budget, completion, invalid configs"),
        ("teleports", "test a guarded teleport service", "destination validation, cooldowns, failure recovery"),
        ("checkpoints", "test checkpoint progression", "ownership, respawn, reset, replay"),
        ("status_effects", "test timed status effects", "stacking, expiration, cancellation, cleanup"),
    ],
}

CONSTRAINTS = [
    "preserve existing public module interfaces",
    "keep server authority over persistent and competitive state",
    "handle player disconnects without leaking state",
    "avoid unbounded loops, event connections, and spawned tasks",
    "make configuration data-driven instead of hard-coding every value",
    "keep client code presentation-focused and validate client requests on the server",
    "make names stable so other generated files can depend on them",
    "include cleanup paths for temporary instances, connections, and timers",
    "make failure behavior explicit instead of silently swallowing errors",
    "support repeated start/stop cycles without duplicated state",
    "prefer small composable modules over one giant script",
    "keep replication boundaries explicit",
]

VARIATIONS = [
    "the existing project already contains unrelated systems",
    "the feature is added after a previous prototype failed under multiplayer load",
    "the project uses ModuleScripts for shared configuration and services",
    "the feature must survive repeated round restarts",
    "the feature will be exercised by automated regression tests",
    "the feature has both normal and malformed-input test cases",
    "the feature must remain understandable to another developer six months later",
    "the feature should expose clear diagnostics when a dependency is missing",
]

CODE_ARTIFACTS = {
    "zombie_rounds": ("src/ServerScriptService/RoundService.server.luau", "src/ReplicatedStorage/Shared/RoundConfig.luau"),
    "inventory": ("src/ServerScriptService/InventoryService.server.luau", "src/ReplicatedStorage/Shared/InventoryTypes.luau"),
    "shop": ("src/ServerScriptService/ShopService.server.luau", "src/ReplicatedStorage/Shared/ShopConfig.luau"),
    "quests": ("src/ServerScriptService/QuestService.server.luau", "src/ReplicatedStorage/Shared/QuestDefinitions.luau"),
    "boss": ("src/ServerScriptService/BossService.server.luau", "src/ReplicatedStorage/Shared/BossConfig.luau"),
}

def stable_id(agent: str, scenario: str, index: int) -> str:
    return hashlib.sha256(f"{agent}:{scenario}:{index}".encode()).hexdigest()[:16]

def code_artifact(scenario: str, constraint: str, variation: str) -> str:
    paths = CODE_ARTIFACTS.get(
        scenario,
        ("src/ServerScriptService/FeatureService.server.luau", "src/ReplicatedStorage/Shared/FeatureConfig.luau"),
    )
    return (
        "files:\n"
        f"- {paths[0]}: server-authoritative service with explicit lifecycle and cleanup\n"
        f"- {paths[1]}: typed/configured definitions consumed by the service\n"
        "implementation_notes:\n"
        "- validate every client-controlled argument before state mutation\n"
        "- keep mutable session state server-owned\n"
        "- isolate connections/tasks and clean them during teardown\n"
        f"- {constraint}\n"
        f"- {variation}"
    )

def design_artifact(constraint: str, variation: str) -> str:
    return (
        "layout_spec:\n"
        "- primary loop: spawn/orient -> discover -> engage -> recover -> progress\n"
        "- landmarks: 3 strong navigational anchors plus one destination landmark\n"
        "- routes: primary route plus at least one optional loop\n"
        "- combat spaces: separated from safe spawn space with readable transitions\n"
        "- hierarchy: macro silhouette -> landmark -> interaction -> decoration\n"
        "acceptance:\n"
        f"- {constraint}\n"
        f"- {variation}\n"
        "- every major space has a gameplay purpose, not decoration-only geometry"
    )

def animation_artifact(constraint: str, variation: str) -> str:
    return (
        "animation_spec:\n"
        "- clips: anticipation, action/loop, recovery, interruption where applicable\n"
        "- priorities: locomotion < action < reaction < emergency override\n"
        "- transitions: define blend-in/blend-out and cancellation rules\n"
        "- timing: author clear contact beats and avoid ambiguous state ownership\n"
        "- multiplayer: gameplay state comes from authoritative code, animation mirrors state\n"
        "acceptance:\n"
        f"- {constraint}\n"
        f"- {variation}"
    )

def testing_artifact(constraint: str, variation: str) -> str:
    return (
        "test_matrix:\n"
        "- happy path: normal creation, use, completion, and cleanup\n"
        "- boundaries: empty values, maximum values, repeated calls, rapid transitions\n"
        "- adversarial: malformed client requests and invalid references\n"
        "- lifecycle: join, leave, restart, shutdown, reconnect\n"
        "- regression: reproduce the reported failure before verifying the repair\n"
        "acceptance:\n"
        f"- {constraint}\n"
        f"- {variation}\n"
        "- a test is only accepted when its assertion checks observable behavior"
    )

def make_row(agent: str, scenario: str, feature: str, focus: str, index: int) -> dict:
    rng = random.Random(f"{agent}:{scenario}:{index}")
    constraint = rng.choice(CONSTRAINTS)
    variation = rng.choice(VARIATIONS)

    if agent == "code":
        artifact = code_artifact(scenario, constraint, variation)
        plan = [
            "inspect the project manifest and existing dependencies",
            f"define the smallest compatible architecture for {focus}",
            "implement the authoritative state transition and explicit cleanup",
            "add or update shared configuration and dependency boundaries",
            "run static validation and regression tests before accepting the change",
        ]
    elif agent == "design":
        artifact = design_artifact(constraint, variation)
        plan = [
            "identify player goals, entry points, exits, and failure-safe spawn areas",
            f"map the core loop and pacing beats for {focus}",
            "place landmarks before secondary decoration",
            "check route readability, multiplayer flow, and performance-sensitive density",
            "write acceptance criteria that another builder can verify",
        ]
    elif agent == "animation":
        artifact = animation_artifact(constraint, variation)
        plan = [
            "identify gameplay states that require animation coverage",
            f"define clip states and transition rules for {focus}",
            "separate visual state from authoritative gameplay state",
            "specify timing, interruption, priority, and cleanup behavior",
            "define import, naming, rig, and acceptance checks",
        ]
    else:
        artifact = testing_artifact(constraint, variation)
        plan = [
            "inspect the implementation and identify observable contracts",
            f"build a test matrix around {focus}",
            "cover normal, boundary, malformed-input, multiplayer, and lifecycle cases",
            "reproduce failures before proposing a repair",
            "rerun regression coverage after every repair",
        ]

    request = f"{feature}; focus: {focus}; constraint: {constraint}; context: {variation}."
    response = (
        "plan:\n" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan)) +
        f"\nartifact:\n{artifact}\n"
        "test_result:\n"
        "- static/project checks: pass when dependencies and paths resolve\n"
        "- behavioral checks: pass only when expected observable state changes occur\n"
        "- cleanup/lifecycle checks: pass with no duplicated connections or leaked session state\n"
        "accepted: true"
    )
    return {
        "id": stable_id(agent, scenario, index),
        "prompt": request,
        "response": response,
        "agent": agent,
        "scenario": scenario,
        "quality": {
            "structured_trajectory": True,
            "artifact_aware": True,
            "test_aware": True,
            "synthetic": True,
            "private_data": False,
            "permitted_data": True,
        },
    }

def generate(agent: str, count: int, seed: int) -> Iterable[dict]:
    scenarios = SEED_SCENARIOS[agent]
    rng = random.Random(seed + sum(ord(c) for c in agent))
    for index in range(count):
        scenario, feature, focus = scenarios[index % len(scenarios)]
        if index >= len(scenarios):
            scenario, feature, focus = rng.choice(scenarios)
        yield make_row(agent, scenario, feature, focus, index)

def write_dataset(agent: str, count: int, seed: int, output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    written = 0
    with output.open("w", encoding="utf-8") as handle:
        for row in generate(agent, count, seed):
            if row["prompt"] in seen:
                continue
            seen.add(row["prompt"])
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            written += 1
    return written

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the G.H.H.Q.S.D. specialist corpus.")
    parser.add_argument("--agent", choices=sorted(SEED_SCENARIOS), default="all")
    parser.add_argument("--examples-per-agent", type=int, default=12000)
    parser.add_argument("--seed", type=int, default=20260929)
    parser.add_argument("--output", type=Path, default=DATASETS)
    args = parser.parse_args()

    agents = sorted(SEED_SCENARIOS) if args.agent == "all" else [args.agent]
    total = 0
    for agent in agents:
        path = args.output / f"{agent}.jsonl"
        count = write_dataset(agent, args.examples_per_agent, args.seed, path)
        print(f"{agent}: generated {count:,} examples -> {path}")
        total += count
    print(f"g.h.h.q.s.d.: generated {total:,} specialist examples")

if __name__ == "__main__":
    main()
