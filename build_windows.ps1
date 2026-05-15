# Build a Windows executable from main.py
# Run this on a Windows machine with Python installed.

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopPath = Join-Path $env:USERPROFILE 'Desktop'
$DistPath = Join-Path $ScriptDir 'dist'
#$DistPath = $DesktopPath  # Uncomment this line to build the EXE directly onto your Desktop.

# Set this to $true if you want the finished EXE copied to the Desktop after building.
$CopyExecutableToDesktop = $false

# Prefer a local project virtual environment if present.
$LocalVenvPython = Join-Path $ScriptDir '.venv\Scripts\python.exe'
if (Test-Path $LocalVenvPython) {
    $PythonExe = $LocalVenvPython
} else {
    $PythonExe = 'python'
}

# Build as a console application so input() and menu interaction work.
$UseConsole = $true

# Optional: choose a custom icon file for the EXE. Use a .ico file here.
$IconFile = Join-Path $ScriptDir '.\python\Github_Icon.ico'
$UseCustomIcon = Test-Path $IconFile

function FailIfLastExitCodeNonZero {
    param([int]$Code)
    if ($Code -ne 0) {
        Write-Error "Command failed with exit code $Code. Stopping build."
        exit $Code
    }
}

Write-Host "Installing dependencies using: $PythonExe"
& $PythonExe -m pip install --upgrade pip
FailIfLastExitCodeNonZero $LASTEXITCODE

& $PythonExe -m pip install --upgrade -r requirements.txt pyinstaller
FailIfLastExitCodeNonZero $LASTEXITCODE

$pyInstallerArgs = @(
    '--onefile'
    'main.py'
    "--distpath=$DistPath"
    "--workpath=$ScriptDir\build"
    "--specpath=$ScriptDir\build"
)

if (-not $UseConsole) {
    $pyInstallerArgs += '--noconsole'
}

if ($UseCustomIcon) {
    Write-Host "Using icon file: $IconFile"
    $pyInstallerArgs += "--icon=$IconFile"
} else {
    Write-Host "No custom icon found at $IconFile. Building without a custom EXE icon."
}

Write-Host "Running PyInstaller using: $PythonExe"
& $PythonExe -m PyInstaller @pyInstallerArgs
FailIfLastExitCodeNonZero $LASTEXITCODE

Write-Host "Build complete. The executable is in $DistPath"

if ($CopyExecutableToDesktop) {
    $exeName = 'main.exe'
    $builtExe = Join-Path $DistPath $exeName
    if (Test-Path $builtExe) {
        $desktopExe = Join-Path $DesktopPath $exeName
        Copy-Item $builtExe $desktopExe -Force
        Write-Host "Copied built executable to Desktop: $desktopExe"
    } else {
        Write-Warning "Built executable not found at $builtExe."
    }
}
