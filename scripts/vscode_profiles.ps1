Param(
  [Parameter(Mandatory=$true)][ValidateSet("purge","install")][string]$Action
)

$ErrorActionPreference = "Stop"

function Profile-Exists([string]$ProfileName) {
  try {
    & code --list-extensions --profile $ProfileName | Out-Null
    return $true
  } catch {
    return $false
  }
}

# Curated extension sets (edit to taste)
$DevExt = @(
  "GitHub.copilot",
  "GitHub.copilot-chat",
  "GitHub.vscode-pull-request-github",
  "dbaeumer.vscode-eslint",
  "esbenp.prettier-vscode",
  "ms-python.python",
  "ms-python.vscode-pylance",
  "ms-azuretools.vscode-docker",
  "ms-vscode-remote.remote-ssh",
  "ms-vscode-remote.remote-containers",
  "redhat.vscode-yaml",
  "yzhang.markdown-all-in-one"
)

$CyberExt = @($DevExt) # add more only if needed
$InfraExt = @(
  "ms-azuretools.vscode-docker",
  "ms-vscode-remote.remote-ssh",
  "redhat.vscode-yaml",
  "yzhang.markdown-all-in-one"
)

function Purge-Profile([string]$ProfileName) {
  Write-Host "Purging extensions from profile: $ProfileName"
  if (-not (Profile-Exists $ProfileName)) {
    Write-Host "Profile not found: $ProfileName (create once via UI: Profiles: Create Profile)"
    return
  }
  $exts = & code --list-extensions --profile $ProfileName
  foreach ($ext in $exts) {
    if ([string]::IsNullOrWhiteSpace($ext)) { continue }
    & code --profile $ProfileName --uninstall-extension $ext | Out-Null
  }
}

function Install-Profile([string]$ProfileName, [string[]]$Extensions) {
  Write-Host "Installing extensions into profile: $ProfileName"
  if (-not (Profile-Exists $ProfileName)) {
    Write-Host "Profile not found: $ProfileName (create once via UI: Profiles: Create Profile)"
    return
  }
  foreach ($ext in $Extensions) {
    & code --profile $ProfileName --install-extension $ext | Out-Null
  }
}

switch ($Action) {
  "purge" {
    Purge-Profile "Dev"
    Purge-Profile "Cyber"
    Purge-Profile "Infra"
  }
  "install" {
    Install-Profile "Dev" $DevExt
    Install-Profile "Cyber" $CyberExt
    Install-Profile "Infra" $InfraExt
  }
}
