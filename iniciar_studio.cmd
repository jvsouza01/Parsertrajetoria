@echo off
title Parser Trajetoria Studio
color 0B

echo ========================================================
echo   INICIANDO PARSER TRAJETORIA STUDIO
echo   Interface Interativa para Extracao de Provas
echo ========================================================
echo.

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado no sistema!
    echo Por favor, instale o Python 3.10+ para executar o Studio.
    pause
    exit /b 1
)

echo [OK] Iniciando o servidor e abrindo seu navegador...
python run_studio.py

pause
