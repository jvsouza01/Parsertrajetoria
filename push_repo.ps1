$git = "C:\Users\luisd\AppData\Local\GitHubDesktop\app-3.6.4\resources\app\git\cmd\git.exe"

# Configure PATH for this session
$env:Path = "$([System.IO.Path]::GetDirectoryName($git));" + $env:Path

Write-Host "--- Git Init & Remote ---"
if (-not (Test-Path ".git")) {
    & $git init
    & $git remote add origin https://github.com/jvsouza01/Parsertrajetoria.git
}

# Fetch remote info
Write-Host "--- Fetching Remote ---"
& $git fetch origin main

# Check branch
& $git branch -M main

# If remote main exists, soft reset or sync
& $git reset origin/main

Write-Host "--- Git Add & Commit ---"
& $git add .
& $git commit -m "feat: implementa parser, modelos de conformidade legal e datasets de questoes PMBA"

Write-Host "--- Git Push ---"
& $git push -u origin main
