"""
Configuração do sistema, detecção de motores LLM (Google Gemini & Ollama) e servidor.
Baseado na infraestrutura madura multiagente do laboratório ER0_DeV.
"""

import os
import subprocess
import urllib.request
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# 1. Configurações do Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
GEMINI_CANDIDATE_MODELS = [
    GEMINI_MODEL,
    "gemini-flash-latest",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
    "gemini-3.5-flash-lite",
]

# 2. Configurações do Ollama Local
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")
OLLAMA_FALLBACK_MODEL = os.getenv("OLLAMA_FALLBACK_MODEL", "deepseek-r1:7b")


def resolve_ollama_host() -> str:
    """
    Resolve o host do Ollama:
    1. Verifica OLLAMA_HOST explícito no ambiente.
    2. Testa localhost:11434.
    3. Se estiver no Windows e falhar, busca o IP do WSL Ubuntu dinamicamente.
    """
    env_host = os.getenv("OLLAMA_HOST")
    if env_host:
        return env_host

    # 1. Tenta localhost
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=0.8)
        return "http://localhost:11434"
    except Exception:
        pass

    # 2. Tenta IP do WSL Ubuntu (caso o Ollama rode dentro do WSL)
    try:
        out = subprocess.check_output(
            ["wsl", "-d", "Ubuntu", "hostname", "-I"], text=True, timeout=2.0
        ).strip().split()[0]
        wsl_host = f"http://{out}:11434"
        urllib.request.urlopen(f"{wsl_host}/api/tags", timeout=1.0)
        return wsl_host
    except Exception:
        pass

    return "http://localhost:11434"


# 3. Configurações do Servidor Web
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", os.getenv("SERVER_PORT", "5005")))

# 4. Regras de Negócio Multiagente
MAX_AUDIT_ITERATIONS = int(os.getenv("MAX_AUDIT_ITERATIONS", "3"))
MIN_PASSING_SCORE = float(os.getenv("MIN_PASSING_SCORE", "8.5"))
