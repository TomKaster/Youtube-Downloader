# Builds dist\ytdownloader.exe with Deno and ffmpeg packed inside,
# so end users only need the single .exe.
#
# Run from this folder:
#   powershell -ExecutionPolicy Bypass -File build.ps1
#
# Delete the bin\ folder to force fresh copies of deno/ffmpeg on the next build.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'   # makes Invoke-WebRequest much faster
Set-Location $PSScriptRoot

$bin = Join-Path $PSScriptRoot 'bin'
New-Item -ItemType Directory -Force $bin | Out-Null
$tmp = Join-Path $env:TEMP 'ytdownloader-build'
New-Item -ItemType Directory -Force $tmp | Out-Null

function Get-ExeFromZip($url, $exeName) {
    $zip = Join-Path $tmp "$exeName.zip"
    $out = Join-Path $tmp "$exeName-extract"
    Write-Host "Downloading $exeName ..."
    Invoke-WebRequest $url -OutFile $zip
    if (Test-Path $out) { Remove-Item $out -Recurse -Force }
    Expand-Archive $zip -DestinationPath $out
    $exe = Get-ChildItem $out -Recurse -Filter $exeName | Select-Object -First 1
    if (-not $exe) { throw "$exeName not found in $url" }
    Copy-Item $exe.FullName (Join-Path $bin $exeName) -Force
}

if (-not (Test-Path "$bin\deno.exe")) {
    Get-ExeFromZip 'https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip' 'deno.exe'
}
if (-not (Test-Path "$bin\ffmpeg.exe")) {
    Get-ExeFromZip 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' 'ffmpeg.exe'
}

Write-Host "Installing/updating Python packages ..."
py -m pip install -U -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }

Write-Host "Building executable ..."
py -m PyInstaller --onefile --clean --noconfirm `
    --name ytdownloader `
    --collect-data yt_dlp_ejs `
    --add-binary "bin\deno.exe;." `
    --add-binary "bin\ffmpeg.exe;." `
    ytdownloader.py
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }

Write-Host ""
Write-Host "Done: dist\ytdownloader.exe (Deno and ffmpeg included)"
