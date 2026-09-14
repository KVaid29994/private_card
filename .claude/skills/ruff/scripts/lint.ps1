# Lint a path with Ruff and print a summary.
# Usage: ./lint.ps1 [path]

param(
    [string]$Path = "."
)

if (-not (Get-Command ruff -ErrorAction SilentlyContinue)) {
    Write-Error "ruff is not installed. Run: pip install ruff"
    exit 1
}

ruff check $Path
