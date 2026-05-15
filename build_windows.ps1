# Build a Windows executable from main.py
# Run this on a Windows machine with Python installed.
#
# HOW TO BUMP VERSION:
#   Edit version.py and increment __version__ (e.g., 1.0.0 -> 1.0.1)
#   Run this script to rebuild with the new version
#
# HOW TO RELEASE TO GITHUB:
#   1. Commit your changes: git add . && git commit -m "v{version}"
#   2. Tag the commit: git tag v{version}
#   3. Push: git push origin main && git push origin v{version}
#   4. Create release on GitHub and attach the built EXE from dist/
#
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

# Read the version from version.py
$VersionMatch = Select-String -Path (Join-Path $ScriptDir 'version.py') -Pattern '__version__ = "([^"]+)"' | Select-Object -First 1
if ($VersionMatch) {
    $AppVersion = $VersionMatch.Matches.Groups[1].Value
} else {
    $AppVersion = "1.0.0"
}

# Read app name from version.py
$AppNameMatch = Select-String -Path (Join-Path $ScriptDir 'version.py') -Pattern '__app_name__ = "([^"]+)"' | Select-Object -First 1
if ($AppNameMatch) {
    $AppName = $AppNameMatch.Matches.Groups[1].Value
} else {
    $AppName = "main"
}

$ExeName = "$AppName"

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
    "--name=$ExeName"
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
Write-Host "App: $AppName v$AppVersion"

if ($CopyExecutableToDesktop) {
    $exeFileName = "$ExeName.exe"
    $builtExe = Join-Path $DistPath $exeFileName
    if (Test-Path $builtExe) {
        $desktopExe = Join-Path $DesktopPath $exeFileName
        Copy-Item $builtExe $desktopExe -Force
        Write-Host "Copied built executable to Desktop: $desktopExe"
    } else {
        Write-Warning "Built executable not found at $builtExe."
    }
}
