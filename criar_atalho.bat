@echo off
title Criar Atalho na Area de Trabalho
color 0B

echo ========================================================
echo   CRIANDO / ATUALIZANDO ATALHO NA AREA DE TRABALHO
echo ========================================================
echo.

python gerar_icone.py
python criar_atalho.py

echo.
echo ========================================================
echo   CONCLUIDO COM SUCESSO!
echo ========================================================
pause
