# airo ai runtime

the python layer owns model providers, agent orchestration, project memory, tools, generation, evaluation, and training data preparation.

the native windows and macos shells communicate with the runtime through newline-delimited json. the runtime can stream progress while chat and code work continue independently.

the default echo provider is deterministic and exists for tests/offline development. real providers implement the same provider protocol.

private project content is not automatically added to training data.
