# airobloxbuilder architecture

airobloxbuilder is a native desktop application.

## platform shells

- windows: c# / wpf
- macos: swift / swiftui

the platform shells own native windows, menus, dialogs, packaging, and platform integration.

## shared engine

rust is the primary shared systems layer. platform shells communicate with it through a small stable api.

## core libraries

1. airo-core: shared types and events
2. airo-project: project state and filesystem model
3. airo-orchestrator: agent coordination
4. airo-agents: internal agent runtime
5. airo-planner: living plans and dependency graphs
6. airo-tasks: task lifecycle
7. airo-memory: project context and history
8. airo-models: model/provider abstraction
9. airo-tools: tool execution
10. airo-roblox: roblox project integration
11. airo-luau: luau generation and analysis
12. airo-assets: asset pipeline
13. airo-animation: animation pipeline
14. airo-audio: music and sound pipeline
15. airo-networking: multiplayer/networking helpers
16. airo-testing: test orchestration
17. airo-repair: diagnosis and repair loops
18. airo-mcp: mcp capability discovery and transport

## language boundaries

c# handles the windows shell and powershell integration.

swift handles the macos shell.

rust handles shared native infrastructure.

c++ is reserved for performance-sensitive native modules.

python handles training, datasets, evaluation, and research tooling.

typescript and javascript handle protocol adapters and compatibility integrations.

luau and lua handle roblox code and lua ecosystem compatibility.

go handles small infrastructure utilities.

kotlin is reserved for future android tooling.

sql handles structured local project data.

bash and powershell handle automation.

yaml defines github actions and other declarative automation.

not every language ships inside the desktop executable. tooling and training languages stay separate from the runtime when possible.

## dependency rule

higher layers may depend on lower layers, but libraries should not reach sideways into unrelated libraries.

```text
native shell
    ↓
application api
    ↓
rust core
    ↓
orchestrator
    ↓
agents
    ↓
tools / integrations
    ↓
roblox
```

the goal is a large system with small, understandable boundaries.
