$ErrorActionPreference = "Stop"

Write-Host "building airobloxbuilder native stack"
cargo test --manifest-path src/core/Cargo.toml
if (Get-Command python -ErrorAction SilentlyContinue) {
  $env:PYTHONPATH = "src/ai"
  python -m pytest src/ai/tests
}
dotnet build src/windows/AiroRobloxBuilder.csproj
Write-Host "native stack validation complete"
