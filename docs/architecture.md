# airobloxbuilder architecture

airobloxbuilder is a native desktop studio for building roblox games through natural-language orchestration.

## build order

1. native ui
2. native/shared logic
3. python ai logic
4. deeper project/task logic
5. generation and model handling
6. runtime systems
7. cross-language integration
8. release packaging

this keeps generation from becoming tightly coupled to the ui or a specific model provider.

## platform shells

- windows: c# / wpf
- macos: swift / swiftui

the shells own native windows, menus, dialogs, onboarding, platform integration, and packaging.

## shared native logic

rust is the stable shared systems layer.

c++ is used behind a small ffi boundary for native utilities where lower-level performance or platform access is useful. rust remains the owner of the public data model.

current core areas include requests, orchestration, project snapshots, task graphs, workspace changes, system capabilities, and onboarding state.

## ai logic

python owns provider-neutral ai orchestration primitives:

- request and response contracts
- agent routing
- plan generation
- generation jobs
- model registry/provider interface

the ai layer does not assume a particular vendor or model.

## generation and model handling

generation is split from model access.

the model layer answers how to ask the configured model for a response.

the generation layer answers what requests should be produced for a build job and how those requests map to planned work.

## runtime systems

runtime systems cover persistent state and external capabilities, including onboarding progress, roblox studio mcp state, filesystem/process capability discovery, and future provider configuration.

mcp is optional. the app must never claim capabilities that the connected interface does not expose.

## cross-language boundary

- c# handles the windows shell and powershell integration.
- swift handles the macos shell.
- rust handles shared native infrastructure.
- c++ handles selected native utilities.
- python handles ai orchestration, training, datasets, evaluation, and research tooling.
- typescript defines protocol/event contracts and compatibility adapters.
- javascript is available for compatible integrations.
- luau/lua handle roblox code and lua ecosystem compatibility.
- go handles small infrastructure utilities.
- kotlin is reserved for future android tooling.
- sql is reserved for structured local project data.
- bash/powershell handle automation.
- yaml defines github actions.

heavy training data, model weights, sdk packs, and development toolchains remain optional whenever possible.

## core library map

1. airo-core
2. airo-project
3. airo-orchestrator
4. airo-agents
5. airo-planner
6. airo-tasks
7. airo-memory
8. airo-models
9. airo-tools
10. airo-roblox
11. airo-luau
12. airo-assets
13. airo-animation
14. airo-audio
15. airo-networking
16. airo-testing
17. airo-repair
18. airo-mcp

these are architectural boundaries. they do not all need to become separate operating-system packages.

## dependency direction

native ui
  -> application api
  -> rust core
  -> ai planning
  -> generation
  -> agents and tools
  -> roblox integration

the goal is a large system with small, understandable boundaries and a small native application footprint.
