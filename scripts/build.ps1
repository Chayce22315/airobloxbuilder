$ErrorActionPreference = "Stop"
dotnet publish src/windows/AiroRobloxBuilder.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -o artifacts/windows
Write-Host "windows artifact ready"