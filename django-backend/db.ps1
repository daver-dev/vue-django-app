param(
    [ValidateSet('start', 'stop', 'logs', 'status')]
    [string]$Action = 'up'
)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

switch ($Action) {
    'start' {
        docker compose up -d
        Write-Output "Postgres is starting. Check status with: .\db.ps1 status"
    }
    'stop' {
        docker compose down
    }
    'logs' {
        docker compose logs -f db
    }
    'status' {
        docker compose ps
    }
}
