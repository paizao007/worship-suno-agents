#!/bin/bash
cd "$(dirname "$0")"

echo "======================================================================"
echo "  🕊️ INICIANDO BANDA LVS LITÚRGICA MULTIAGENTE & SUNO AI 🎵 (LINUX/WSL)"
echo "======================================================================"

if [ -f .env ]; then
    set -a
    . .env
    set +a
fi

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

PORT="${1:-5005}"
echo "[*] Iniciando servidor web na porta $PORT..."
echo "[*] Acesse no navegador: http://localhost:$PORT"
python3 server.py --host 0.0.0.0 --port "$PORT"
