"""AI-provider abstraction with a source-based fallback."""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any

import requests

from config import (
    AI_PROVIDER,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)


class AIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError


class GroqProvider(AIProvider):
    def __init__(self) -> None:
        from groq import Groq
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt or "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.35,
            max_tokens=2200,
        )
        return response.choices[0].message.content or ""


class GeminiProvider(AIProvider):
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{GEMINI_MODEL}:generateContent"
        )
        payload: dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.35, "maxOutputTokens": 2200},
        }
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        response = requests.post(
            url,
            headers={"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"},
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]


class OllamaProvider(AIProvider):
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "")


class TemplateProvider(AIProvider):
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return "TEMPLATE_MODE"


def get_ai_provider() -> AIProvider:
    if AI_PROVIDER == "groq" and GROQ_API_KEY:
        return GroqProvider()
    if AI_PROVIDER == "gemini" and GEMINI_API_KEY:
        return GeminiProvider()
    if AI_PROVIDER == "ollama":
        return OllamaProvider()
    return TemplateProvider()


def parse_json_response(response: str) -> dict[str, Any] | None:
    text = response.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, count=1, flags=re.I)
        text = re.sub(r"\s*```$", "", text, count=1)

    start, end = text.find("{"), text.rfind("}")
    candidates = [text]
    if start >= 0 and end > start:
        candidates.insert(0, text[start : end + 1])

    for candidate in candidates:
        try:
            value = json.loads(candidate, strict=False)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None
