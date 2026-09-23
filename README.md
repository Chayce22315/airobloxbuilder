# airobloxbuilder

a free roblox game builder :)

airobloxbuilder is an ai-powered game development studio for roblox. describe the game you want to make, and the builder plans, builds, tests, and improves it.

## the idea

**type the game idea → ai builds the game.**

instead of manually creating every system from scratch, describe what you want in natural language.

for example:

> make a 50-player infection game with 8 maps

the builder can plan the systems required, split the work between specialized agents, create the project, test it, and repair problems it finds.

you can keep modifying an existing project naturally:

> make the mall twice as large

> add a secret basement

> add a giant banana boss

> make rounds last 5 minutes

the builder should understand the existing project and make coordinated changes instead of rebuilding everything from scratch.

## what it can build

the long-term goal is to handle the pieces needed for a complete roblox game:

- luau scripts
- gameplay systems
- maps and worlds
- models and assets
- textures
- characters and skins
- animations
- ui
- music and sound effects
- vfx
- npc behavior
- cutscenes
- save systems
- multiplayer and networking
- testing
- debugging and repair
- optimization

## built-in agent system

airobloxbuilder uses its own internal subagent system.

the main orchestrator decides which specialized agents are needed for a request instead of running every agent every time.

planned agents include:

- 🧠 orchestrator
- 📋 planning
- 💻 code
- 🎮 gameplay
- 🧱 world
- 🎨 assets
- 🎬 animation
- 🎵 audio
- 🖥️ ui
- 🤖 npc
- 🌐 networking
- 🧪 testing
- 🔧 repair/debugging
- ⚡ optimization
- 📚 project/documentation

agents can cooperate through shared project state.

```text
user request
    ↓
🧠 orchestrator
    ↓
📋 plan
    ↓
🧱 world + 🎨 assets
    ↓
💻 code + 🎬 animation
    ↓
🧪 testing
    ↓
🔧 repair
    ↓
🧪 test again
    ↓
✅ finished
```

## /plan

`/plan` turns a game idea or requested change into a living development plan.

it can:

- break a project into phases and tasks
- identify dependencies
- create and maintain todos
- ask questions when a user-specific decision is required
- track completed, active, skipped, and blocked work
- update the plan when the user changes their mind
- add tasks when agents discover missing work

example:

```text
/plan make a 50-player infection game with 8 maps
```

the plan can cover gameplay, maps, ui, audio, networking, saving, testing, optimization, and agent assignments.

## testing and repair

testing is part of the build process.

if something fails, the builder can investigate the failure, attempt a repair, and run the relevant test again.

```text
build
 ↓
test
 ↓
failure
 ↓
diagnose
 ↓
repair
 ↓
test
 ↓
pass
```

## roblox studio mcp

roblox studio mcp support is optional.

mcp is a capability bridge, not an external agent. the builder's own orchestrator and agents remain part of airobloxbuilder.

the builder should detect what the connected mcp actually exposes instead of assuming every mcp supports the same things.

if the mcp exposes the roblox studio project hierarchy, the builder can represent that structure inside its own interface.

the app does **not** assume that a roblox studio viewport or visual preview is available.

## free forever

airobloxbuilder is intended to be completely free.

there are:

- no subscriptions
- no pro or premium tier
- no ai credits
- no generation limits
- no paywalls
- no upgrade prompts
- no monthly plans

**you don't pay to make the game.**

there is no paid version of the builder.

an optional donation/tip area may exist to support development, but donating does not unlock features or provide advantages. it can only provide a small supporter badge.

## project philosophy

the tool should help you make the game, not become another obstacle between you and the game.

natural language is the main interface, while the underlying system handles planning, agents, project state, testing, repair, and integration.

## status

🚧 **early development**

this repository is the home of the airobloxbuilder project and its development infrastructure.

more implementation details will be added as the project grows.

## license

see the repository license for the terms that apply to this project.
