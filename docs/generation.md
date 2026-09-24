# generation pipeline

1. normalize the request
2. snapshot project context
3. route to the required agents
4. ask the configured model for structured work
5. validate generated paths and content
6. write changes through the project system
7. run tests
8. repair failures
9. present the resulting artifacts

models are providers, not the builder itself. the builder keeps orchestration, tools, validation, project memory, and repair logic independent from any single model.