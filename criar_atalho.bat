@echo off
title Criar Atalho na Area de Trabalho
color 0B

echo Criando atalho do Parser Trajetoria Studio na sua Area de Trabalho...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$WshShell = New-Object -comObject WScript.Shell; $Desktop = [Environment]::GetFolderPath('Desktop'); $TargetExe = Join-Path (Get-Location) 'dist\ParserStudio.exe'; if (-not (Test-Path $TargetExe)) { $TargetExe = Join-Path (Get-Location) 'iniciar_studio.bat' }; $IconFile = Join-Path (Get-Location) 'icon.ico'; $Shortcut = $WshShell.CreateShortcut((Join-Path $Desktop 'Parser Trajetoria Studio.lnk')); $Shortcut.TargetPath = $TargetExe; $Shortcut.WorkingDirectory = (Get-Location).Path; if (Test-Path $IconFile) { $Shortcut.IconLocation = $IconFile }; $Shortcut.Description = 'Parser Trajetoria Studio'; $Shortcut.Save(); Write-Host '[OK] Atalho criado com sucesso na Area de Trabalho!'"

echo.
pause
