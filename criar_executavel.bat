@echo off
title Gerador de Executavel - Parser Trajetoria Studio
color 0A

echo ========================================================
echo   GERANDO EXECUTAVEL COM ICONE (ParserStudio.exe)
echo ========================================================
echo.

python gerar_icone.py

pyinstaller --noconfirm --onefile --name "ParserStudio" --icon="icon.ico" --add-data "templates;templates" --add-data "static;static" main_desktop.py

echo.
echo ========================================================
echo   EXECUTAVEL COM ICONE GERADO NA PASTA: dist\
echo ========================================================
pause
