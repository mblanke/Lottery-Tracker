Param(
  [Parameter(Mandatory=$false)][string]$Command = "status",
  [Parameter(Mandatory=$false)][string]$RepoPath = ""
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

Write-Host "== Dev Backbone Monday Runner =="

function Need-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Missing command: $name"
  }
}

switch ($Command) {
  "status" {
    $code = (Get-Command code -ErrorAction SilentlyContinue)
    $git = (Get-Command git -ErrorAction SilentlyContinue)
    $docker = (Get-Command docker -ErrorAction SilentlyContinue)

    Write-Host "[1] VS Code CLI:" ($code.Source ?? "NOT FOUND")
    Write-Host "[2] Git:       " ($git.Source ?? "NOT FOUND")
    Write-Host "[3] Docker:    " ($docker.Source ?? "NOT FOUND")
    Write-Host ""
    Write-Host "Profiles expected: Dev, Cyber, Infra"
    Write-Host "Try: code --list-extensions --profile Dev"
  }

  "vscode-purge" {
    Need-Cmd code
    if ($env:CONFIRM -ne "YES") {
      Write-Host "Refusing to uninstall extensions without CONFIRM=YES"
      Write-Host "Run: `$env:CONFIRM='YES'; .\scripts\monday.ps1 -Command vscode-purge"
      exit 2
    }
    & (Join-Path $RootDir "scripts\vscode_profiles.ps1") -Action purge
  }

  "vscode-install" {
    Need-Cmd code
    & (Join-Path $RootDir "scripts\vscode_profiles.ps1") -Action install
  }

  "repo-bootstrap" {
    if ([string]::IsNullOrWhiteSpace($RepoPath)) {
      throw "Usage: .\scripts\monday.ps1 -Command repo-bootstrap -RepoPath C:\path\to\repo"
    }
    & (Join-Path $RootDir "scripts\bootstrap_repo.ps1") -RepoPath $RepoPath
  }

  default {
    throw "Unknown command: $Command"
  }
}
