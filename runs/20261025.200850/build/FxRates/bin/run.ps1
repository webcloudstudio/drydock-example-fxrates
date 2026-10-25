$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Activate = Join-Path $Root ".venv\Scripts\Activate.ps1"
if (Test-Path $Activate) { & $Activate }
python -m cli @args
exit $LASTEXITCODE
