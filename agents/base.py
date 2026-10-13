"""
Classe base para todos os agentes do sistema.
Implementa o motor de inteligência artificial multi-provedor com cache de disponibilidade:
1. Google Gemini Cloud API (gemini-flash-latest / gemini-3.6-flash / gemini-3.8-flash)
2. Cloud Generative AI (OpenAI-compatible endpoint com timeout rápido e cooldown automático)
3. Ollama Local / WSL
4. Motor Poético Combinatório Sacro Inédito (Zero repetição garantida)
"""

import json
import re
import time
from abc import ABC, abstractmethod
from typing import Any, Optional, Type
import requests
from pydantic import BaseModel
import config


def extract_json_from_text(text: str) -> Optional[dict]:
    """Extrai objeto JSON válido de uma string, tratando blocos de código ```json."""
    if not text:
        return None
    text = text.strip()
    if "```" in text:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            text = match.group(1).strip()
    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except Exception:
                pass
    return None


class BaseAgent(ABC):
    _gemini_cooldown_until: float = 0.0
    _cloud_cooldown_until: float = 0.0
    _ollama_cooldown_until: float = 0.0

    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt

    @abstractmethod
    def run(self, input_data: Any) -> BaseModel:
        """Executa a tarefa do agente sobre os dados de entrada e retorna o modelo Pydantic esperado."""
        pass

    def call_llm(
        self,
        user_prompt: str,
        response_model: Type[BaseModel],
        custom_json_example: Optional[str] = None,
        temperature: float = 0.88,
    ) -> BaseModel:
        """
        Executa a inferência de IA Generativa com cascata inteligente e zero travamento:
        1. Google Gemini Cloud API (quando dentro da cota diária).
        2. Cloud Generative AI (com cooldown automático se houver lentidão externa).
        3. Ollama Local / WSL.
        4. Motor Poético Combinatório Sacro Inédito (verifica o histórico para jamais repetir).
        """
        if custom_json_example:
            instrucao_formato = (
                f"\n\nIMPORTANTE: Responda EXCLUSIVAMENTE em JSON válido seguindo exatamente esta estrutura:\n"
                f"{custom_json_example}\n"
                "Não adicione texto fora do JSON."
            )
        else:
            schema_json = json.dumps(response_model.model_json_schema(), ensure_ascii=False, indent=2)
            instrucao_formato = (
                f"\n\nIMPORTANTE: Responda EXCLUSIVAMENTE em formato JSON compatível com este schema:\n"
                f"{schema_json}\n"
                "Não adicione texto fora do JSON."
            )

        full_prompt = f"{self.system_prompt}\n\nTarefa:\n{user_prompt}\n{instrucao_formato}"
        now = time.time()

        # 1. Tentativa via Google Gemini Cloud API
        if config.GEMINI_API_KEY and now > getattr(BaseAgent, "_gemini_cooldown_until", 0):
            for model_name in ["gemini-flash-lite-latest", "gemini-2.5-flash-lite", "gemini-flash-latest", "gemini-3.8-flash"]:
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/"
                    f"{model_name}:generateContent?key={config.GEMINI_API_KEY}"
                )
                payload = {
                    "contents": [{"parts": [{"text": full_prompt}]}],
                    "generationConfig": {
                        "temperature": temperature,
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
                            for p in parts:
                                if "text" in p:
                                    parsed = extract_json_from_text(p["text"])
                                    if parsed:
                                        return response_model.model_validate(parsed)
                    elif r.status_code == 429:
                        continue
                except Exception:
                    continue
            BaseAgent._gemini_cooldown_until = now + 60

        # 2. Tentativa via Cloud Generative AI (com timeout curto de 5s e cooldown)
        if now > getattr(BaseAgent, "_cloud_cooldown_until", 0):
            try:
                cloud_res = requests.post(
                    "https://text.pollinations.ai/openai",
                    json={
                        "model": "openai",
                        "messages": [
                            {"role": "system", "content": "Você é um poeta sacro cristão. Responda APENAS JSON válido."},
                            {"role": "user", "content": f"{user_prompt}\n{instrucao_formato}"},
                        ],
                        "temperature": temperature,
                        "seed": int(time.time() * 1000) % 1000000,
                    },
                    timeout=5,
                )
                if cloud_res.status_code == 200:
                    c_json = cloud_res.json()
                    choices = c_json.get("choices", [])
                    if choices:
                        content_str = choices[0].get("message", {}).get("content", "")
                        parsed = extract_json_from_text(content_str)
                        if parsed:
                            return response_model.model_validate(parsed)
                else:
                    BaseAgent._cloud_cooldown_until = now + 300
            except Exception:
                BaseAgent._cloud_cooldown_until = now + 300

        # 3. Tentativa via Ollama Local
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
                o_res = requests.post(o_url, json=o_payload, timeout=3)
                if o_res.status_code == 200:
                    raw_resp = o_res.json().get("response", "")
                    parsed = extract_json_from_text(raw_resp)
                    if parsed:
                        return response_model.model_validate(parsed)
                else:
                    BaseAgent._ollama_cooldown_until = now + 300
            except Exception:
                BaseAgent._ollama_cooldown_until = now + 300

        # 4. Motor Poético Combinatório Sacro Inédito
        return self._generate_contextual_demonstration(user_prompt, response_model)

    @abstractmethod
    def _generate_contextual_demonstration(
        self, user_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """Gera resposta contextual estruturada fiel à teologia e à engenharia do Suno."""
        pass
