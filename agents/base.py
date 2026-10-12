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

        import time
        now = time.time()

        # 1. Tentativa via Google Gemini Cloud API (com circuit-breaker rápido para 429)
        if config.GEMINI_API_KEY and now > getattr(BaseAgent, "_gemini_cooldown_until", 0):
            for model_name in config.GEMINI_CANDIDATE_MODELS[:2]:
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/"
                    f"{model_name}:generateContent?key={config.GEMINI_API_KEY}"
                )
                payload = {
                    "contents": [{"parts": [{"text": full_prompt}]}],
                    "generationConfig": {
                        "temperature": 0.6,
                        "responseMimeType": "application/json",
                    },
                }
                try:
                    r = requests.post(url, json=payload, timeout=8)
                    if r.status_code == 200:
                        data = r.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                parsed = extract_json_from_text(parts[0]["text"])
                                if parsed:
                                    return response_model.model_validate(parsed)
                    elif r.status_code == 429:
                        # Ativa cooldown de 120s para não travar a interface do usuário em chamadas seguidas
                        BaseAgent._gemini_cooldown_until = now + 120
                        break
                except Exception:
                    BaseAgent._gemini_cooldown_until = now + 60
                    break

        # 2. Tentativa rápida via Ollama Local (com circuit-breaker caso esteja lento na CPU)
        if now > getattr(BaseAgent, "_ollama_cooldown_until", 0):
            ollama_host = config.resolve_ollama_host()
            try:
                o_url = f"{ollama_host}/api/generate"
                o_payload = {
                    "model": config.OLLAMA_MODEL,
                    "prompt": full_prompt,
                    "stream": False,
                    "format": "json",
                }
                o_res = requests.post(o_url, json=o_payload, timeout=5)
                if o_res.status_code == 200:
                    raw_resp = o_res.json().get("response", "")
                    parsed = extract_json_from_text(raw_resp)
                    if parsed:
                        return response_model.model_validate(parsed)
                else:
                    BaseAgent._ollama_cooldown_until = now + 180
            except Exception:
                BaseAgent._ollama_cooldown_until = now + 180

        # 3. Motor Teológico e Poético Contextual Dinâmico (Instantâneo)
        return self._generate_contextual_demonstration(user_prompt, response_model)

    @abstractmethod
    def _generate_contextual_demonstration(
        self, user_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """Gera resposta contextual estruturada fiel à teologia e à engenharia do Suno."""
        pass
