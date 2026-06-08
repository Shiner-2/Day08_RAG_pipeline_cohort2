$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Processes = @()

function Stop-PortProcess {
    param([int]$Port)

    $connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    foreach ($connection in $connections) {
        Write-Host "Stopping existing process on port $Port (PID $($connection.OwningProcess))" -ForegroundColor DarkYellow
        Stop-Process -Id $connection.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

function Start-LoggedProcess {
    param(
        [string]$Name,
        [string]$FileName,
        [string]$Arguments
    )

    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $FileName
    $startInfo.Arguments = $Arguments
    $startInfo.WorkingDirectory = $Root
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    $process.EnableRaisingEvents = $true

    Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action {
        if ($EventArgs.Data) {
            Write-Host "[$($Event.MessageData)] $($EventArgs.Data)"
        }
    } -MessageData $Name | Out-Null

    Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action {
        if ($EventArgs.Data) {
            Write-Host "[$($Event.MessageData)] $($EventArgs.Data)" -ForegroundColor DarkRed
        }
    } -MessageData $Name | Out-Null

    [void]$process.Start()
    $process.BeginOutputReadLine()
    $process.BeginErrorReadLine()
    $script:Processes += $process

    Write-Host "Started $Name (PID $($process.Id))" -ForegroundColor Green
    return $process
}

function Wait-Http {
    param(
        [string]$Url,
        [int]$TimeoutSeconds = 60
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
                return $true
            }
        } catch {
            Start-Sleep -Seconds 1
        }
    }
    return $false
}

try {
    Write-Host "Starting Drug Law RAG Chatbot from $Root" -ForegroundColor Cyan

    Stop-PortProcess -Port 8000
    Stop-PortProcess -Port 8501

    Start-LoggedProcess `
        -Name "backend" `
        -FileName "python" `
        -Arguments "-m uvicorn backend:app --host 127.0.0.1 --port 8000"

    if (Wait-Http -Url "http://127.0.0.1:8000/health" -TimeoutSeconds 45) {
        Write-Host "Backend ready:  http://127.0.0.1:8000/docs" -ForegroundColor Green
    } else {
        Write-Host "Backend did not become ready in time. Check logs above." -ForegroundColor Red
    }

    if (Wait-Http -Url "http://127.0.0.1:8000" -TimeoutSeconds 20) {
        Write-Host "Frontend ready: http://127.0.0.1:8000" -ForegroundColor Green
        Start-Process "http://127.0.0.1:8000"
    } else {
        Write-Host "Frontend did not become ready in time. Check logs above." -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "Backend and frontend are running from the same FastAPI server." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C or close this window to stop the app." -ForegroundColor Yellow

    while ($true) {
        foreach ($process in @($Processes)) {
            if ($process.HasExited) {
                Write-Host "Process PID $($process.Id) exited with code $($process.ExitCode)." -ForegroundColor Red
                $script:Processes = @($Processes | Where-Object { -not $_.HasExited })
            }
        }
        Start-Sleep -Seconds 2
    }
} finally {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    foreach ($process in @($Processes)) {
        if ($process -and -not $process.HasExited) {
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        }
    }
}
