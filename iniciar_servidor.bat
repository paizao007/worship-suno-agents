@echo off
chcp 65001 > nul
title 🕊️ Banda LVS Liturgica Multiagente e Suno AI 🎵
cd /d "%~dp0"

echo ======================================================================
echo   🕊️ INICIANDO BANDA LVS LITÚRGICA MULTIAGENTE & SUNO AI 🎵
echo ======================================================================

if not exist ".venv\Scripts\python.exe" (
    echo [!] Ambiente virtual nao encontrado. Criando .venv...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo [*] Iniciando servidor web na porta 5005...
echo [*] Acesse no navegador: http://localhost:5005
echo.

python server.py --host 0.0.0.0 --port 5005

pause
