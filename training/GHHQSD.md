# G.H.H.Q.S.D.

genuinely huge, high-quality specialist dataset

the specialist factory now has a deterministic corpus generator instead of relying on the old tiny seed datasets.

## corpus size

the default corpus is 48,000 structured examples:

- 12,000 coding trajectories
- 12,000 design trajectories
- 12,000 animation/content trajectories
- 12,000 testing trajectories

## what each record teaches

each record contains:

- a concrete roblox development request
- a multi-step specialist plan
- artifact/file expectations
- implementation or design constraints
- test and lifecycle expectations
- an acceptance state
- scenario and quality metadata

the generator rotates through 16 curated scenarios per specialist and a constraint/variation bank. output is deterministic from the seed.

## quality gates

training/quality_gate.py rejects:

- malformed jsonl
- duplicate prompts
- missing trajectory sections
- placeholder text
- private-data flags
- records without artifact/test awareness

## data policy

the corpus is synthetic and explicitly permitted. it does not automatically ingest private projects, user files, github repositories, or internet code.

## generation

generate all four specialists:

python training/generate_ghh_qsd.py

generate one specialist:

python training/generate_ghh_qsd.py --agent code --examples-per-agent 12000

then run:

python training/quality_gate.py training/datasets/code.jsonl --agent code

## learning shape

the target pattern is:

request -> inspect -> plan -> artifact -> test -> accept

code and testing examples emphasize roblox project structure, server/client boundaries, cleanup, validation, and regression behavior.

design examples emphasize player goals, routes, landmarks, pacing, multiplayer readability, and acceptance criteria.

animation examples emphasize gameplay states, timing, transitions, priorities, interruption, and authoritative-state boundaries.

the corpus is generated at training time rather than committed to git, keeping the source repository manageable.
