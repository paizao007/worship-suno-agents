"""
Classe base para todos os agentes do sistema.
Implementa o motor de inteligência artificial híbrido (Google Gemini Cloud API + Ollama Local)
com fallback automático, inspirado na arquitetura de ER0_DeV.
"""

import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
import requests
from pydantic import BaseModel
import config


def extract_json_from_text(text: str) -> Optional[dict]:
    """Extrai objeto JSON válido de uma string, tratando blocos de código ```json."""
    text = text.strip()
    # Remove blocos markdown ```json ... ``` se existirem
    if "```" in text:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            text = match.group(1).strip()
    try:
        return json.loads(text)
    except Exception:
        # Tenta encontrar primeiro { e último }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except Exception:
                pass
    return None


class BaseAgent(ABC):
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt

    @abstractmethod
    def run(self, input_data: Any) -> BaseModel:
        """Executa a tarefa do agente sobre os dados de entrada e retorna o modelo Pydantic esperado."""
        pass

    def call_llm(self, user_prompt: str, response_model: Type[BaseModel]) -> BaseModel:
        """
        Executa a inferência de LLM com cascata de confiabilidade:
        1. Google Gemini Cloud API (com lista de modelos em fallback).
        2. Ollama Local / WSL (deepseek-r1 / qwen2.5-coder).
        3. Fallback de Demonstração Contextual.
        """
        schema_json = json.dumps(response_model.model_json_schema(), ensure_ascii=False, indent=2)
        instrucao_formato = (
            f"\n\nIMPORTANTE: Você deve responder EXCLUSIVAMENTE em formato JSON compatível com este schema:\n"
            f"{schema_json}\n"
            "Não adicione comentários, explicações ou texto fora do JSON."
        )

        full_prompt = f"{self.system_prompt}\n\nTarefa:\n{user_prompt}\n{instrucao_formato}"

        # 1. Tentativa via Google Gemini Cloud API
        if config.GEMINI_API_KEY:
            for model_name in config.GEMINI_CANDIDATE_MODELS:
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/"
                    f"{model_name}:generateContent?key={config.GEMINI_API_KEY}"
                )
                payload = {
                    "contents": [{"parts": [{"text": full_prompt}]}],
                    "generationConfig": {
                        "temperature": 0.4,
                        "responseMimeType": "application/json",
                    },
                }
                try:
                    r = requests.post(url, json=payload, timeout=25)
                    if r.status_code == 200:
                        data = r.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                parsed = extract_json_from_text(parts[0]["text"])
                                if parsed:
                                    # print(f"[{self.name}] [+] Sucesso via Gemini ({model_name})")
                                    return response_model.model_validate(parsed)
                    elif r.status_code == 429:
                        # Rate limit: continua para o próximo modelo candidato ou Ollama
                        continue
                except Exception:
                    pass

        # 2. Tentativa via Ollama Local / WSL
        ollama_host = config.resolve_ollama_host()
        candidate_ollama_models = [config.OLLAMA_MODEL, config.OLLAMA_FALLBACK_MODEL, "qwen2.5-coder:7b"]
        for o_model in candidate_ollama_models:
            try:
                o_url = f"{ollama_host}/api/generate"
                o_payload = {
                    "model": o_model,
                    "prompt": full_prompt,
                    "stream": False,
                    "format": "json",
                }
                o_res = requests.post(o_url, json=o_payload, timeout=30)
                if o_res.status_code == 200:
                    raw_resp = o_res.json().get("response", "")
                    parsed = extract_json_from_text(raw_resp)
                    if parsed:
                        # print(f"[{self.name}] [+] Sucesso via Ollama ({o_model}) em {ollama_host}")
                        return response_model.model_validate(parsed)
            except Exception:
                pass

        # 3. Fallback de Demonstração Contextual de alta qualidade
        # print(f"[{self.name}] [!] Utilizando motor analítico contextual para este ciclo.")
        return self._generate_contextual_demonstration(user_prompt, response_model)

    @abstractmethod
    def _generate_contextual_demonstration(
        self, user_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """Gera resposta contextual estruturada fiel à teologia e à engenharia do Suno."""
        pass
