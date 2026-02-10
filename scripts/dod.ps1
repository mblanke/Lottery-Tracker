
$ErrorActionPreference = "Stop"
Write-Host "== DoD Gate =="

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

function Has-Command($name) {
  return $null -ne (Get-Command $name -ErrorAction SilentlyContinue)
}

$hasNode = Test-Path ".\package.json"
$hasPy = (Test-Path ".\pyproject.toml") -or (Test-Path ".\requirements.txt") -or (Test-Path ".\requirements-dev.txt")

if ($hasNode) {
  if (-not (Has-Command "npm")) { throw "npm not found" }
  Write-Host "+ npm ci"; npm ci
  $pkg = Get-Content ".\package.json" | ConvertFrom-Json
  if ($pkg.scripts.lint) { Write-Host "+ npm run lint"; npm run lint }
  if ($pkg.scripts.typecheck) { Write-Host "+ npm run typecheck"; npm run typecheck }
  if ($pkg.scripts.test) { Write-Host "+ npm test"; npm test }
  if ($pkg.scripts.build) { Write-Host "+ npm run build"; npm run build }
}

if ($hasPy) {
  if (-not (Has-Command "python")) { throw "python not found" }
  Write-Host "+ python -m pip install -U pip"; python -m pip install -U pip
  if (Test-Path ".\requirements.txt") { Write-Host "+ pip install -r requirements.txt"; pip install -r requirements.txt }
  if (Test-Path ".\requirements-dev.txt") { Write-Host "+ pip install -r requirements-dev.txt"; pip install -r requirements-dev.txt }
  if (Has-Command "ruff") {
    Write-Host "+ ruff check ."; ruff check .
    Write-Host "+ ruff format --check ."; ruff format --check .
  }
  if (Has-Command "pytest") { Write-Host "+ pytest -q"; pytest -q }
}

if (-not $hasNode -and -not $hasPy) {
  Write-Host "No package.json or Python dependency files detected."
  Write-Host "Customize scripts\dod.ps1 for this repo stack."
}

Write-Host "DoD PASS"
