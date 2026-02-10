Param(
  [Parameter(Mandatory=$true)][string]$RepoPath
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Target = (Resolve-Path $RepoPath).Path

New-Item -ItemType Directory -Force -Path (Join-Path $Target ".claude\agents") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Target "SKILLS") | Out-Null

Copy-Item -Force (Join-Path $RootDir "AGENTS.md") (Join-Path $Target "AGENTS.md")
if (Test-Path (Join-Path $RootDir "SKILLS.md")) {
  Copy-Item -Force (Join-Path $RootDir "SKILLS.md") (Join-Path $Target "SKILLS.md")
}
Copy-Item -Recurse -Force (Join-Path $RootDir "SKILLS\*") (Join-Path $Target "SKILLS")
Copy-Item -Recurse -Force (Join-Path $RootDir ".claude\agents\*") (Join-Path $Target ".claude\agents")

if (-not (Test-Path (Join-Path $Target ".gitlab-ci.yml")) -and (Test-Path (Join-Path $RootDir ".gitlab-ci.yml"))) {
  Copy-Item -Force (Join-Path $RootDir ".gitlab-ci.yml") (Join-Path $Target ".gitlab-ci.yml")
}
if (-not (Test-Path (Join-Path $Target ".github")) -and (Test-Path (Join-Path $RootDir ".github"))) {
  Copy-Item -Recurse -Force (Join-Path $RootDir ".github") (Join-Path $Target ".github")
}

Write-Host "Bootstrapped repo: $Target"
Write-Host "Next: wire DoD gates to your stack and run scripts\dod.ps1"
