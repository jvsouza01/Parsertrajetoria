@echo off
title Gerador de Executavel - Parser Trajetoria Studio
color 0A

echo ========================================================
echo   GERANDO EXECUTAVEL STANDALONE (ParserStudio.exe)
echo ========================================================
echo.

pyinstaller --noconfirm --onefile --name "ParserStudio" --add-data "templates;templates" --add-data "static;static" main_desktop.py

echo.
echo ========================================================
echo   EXECUTAVEL GERADO COM SUCESSO NA PASTA: dist\
echo ========================================================
pause
