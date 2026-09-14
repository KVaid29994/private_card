# Remove the background from an image via the bundled Python script.
# Usage: ./remove_bg.ps1 -InputPath "photo.jpg" [-OutputPath "photo_nobg.png"] [-Matting]

param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [string]$OutputPath,

    [switch]$Matting
)

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "python is not on PATH."
    exit 1
}

$scriptPath = Join-Path $PSScriptRoot "remove_bg.py"
$pyArgs = @($scriptPath, $InputPath)
if ($OutputPath) { $pyArgs += $OutputPath }
if ($Matting) { $pyArgs += "--matting" }

python @pyArgs
