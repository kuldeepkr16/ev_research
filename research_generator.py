"""Turn a source article into an EV/VCU learning and interview brief."""

from __future__ import annotations

from typing import Any

from ai_providers import TemplateProvider, get_ai_provider, parse_json_response
from config import LEARNING_FOCUS


CATEGORY_CONCEPTS = {
    "Communication": ["CAN FD / CAN XL", "Automotive Ethernet", "SOME/IP", "TSN"],
    "Software Architecture": ["AUTOSAR Classic", "AUTOSAR Adaptive", "zonal architecture", "SDV"],
    "Diagnostics & OTA": ["UDS", "DoIP", "OTA update pipeline", "diagnostic services"],
    "Safety & Process": ["ISO 26262", "ASPICE", "traceability", "safety lifecycle"],
    "Testing & Validation": ["MIL", "SIL", "HIL", "virtual ECU"],
    "EV Powertrain": ["VCU", "torque coordination", "battery limits", "inverter control"],
    "Cybersecurity": ["ISO/SAE 21434", "UNECE R155", "secure boot", "threat analysis"],
    "Development Tools": ["CI/CD", "calibration", "CANoe/CANalyzer", "model-based development"],
}


class ResearchGenerator:
    def __init__(self) -> None:
        self.provider = get_ai_provider()

    def generate(self, article: dict[str, Any]) -> dict[str, Any]:
        if isinstance(self.provider, TemplateProvider):
            return self._template(article)

        prompt = f"""
{LEARNING_FOCUS}

Create a factual learning brief from the source metadata below. Do not invent
facts that are not supported by the title/description. If the description is
thin, keep claims conservative and use the source link as the reader's next
step.

SOURCE TITLE: {article.get('title', '')}
SOURCE DESCRIPTION: {article.get('description', '')[:1800]}
SOURCE/PUBLISHER: {article.get('source', '')}
CATEGORY: {article.get('category', '')}

Return valid JSON only with this schema:
{{
  "headline": "short learning-focused headline",
  "summary": "2-4 concise sentences about what the source reports",
  "why_it_matters": "2-3 sentences connecting it to VCU/EV embedded work",
  "key_concepts": ["3-5 concepts or technologies worth learning"],
  "interview_questions": ["2 realistic interview questions"],
  "next_step": "one concrete topic or exercise to study next"
}}
"""
        system = (
            "You are an automotive embedded software research assistant. "
            "Be technically precise, conservative with claims, and return JSON only."
        )
        try:
            response = self.provider.generate(prompt, system)
            parsed = parse_json_response(response)
        except Exception as exc:
            print(f"AI generation warning: {type(exc).__name__}: {exc}")
            parsed = None

        if not parsed:
            return self._template(article)

        result = self._template(article)
        for field in ("headline", "summary", "why_it_matters", "next_step"):
            value = parsed.get(field)
            if isinstance(value, str) and value.strip():
                result[field] = value.strip()
        for field in ("key_concepts", "interview_questions"):
            value = parsed.get(field)
            if isinstance(value, list):
                cleaned = [str(item).strip() for item in value if str(item).strip()]
                if cleaned:
                    result[field] = cleaned[:5]
        result["generation_mode"] = "ai"
        return result

    @staticmethod
    def _template(article: dict[str, Any]) -> dict[str, Any]:
        category = article.get("category", "Automotive Software")
        concepts = CATEGORY_CONCEPTS.get(category, ["embedded software", "VCU", "automotive systems"])
        description = article.get("description", "").strip()
        summary = description or (
            "This source covers a recent development relevant to automotive "
            "embedded software. Open the source article for the full technical context."
        )
        return {
            "id": article.get("id", ""),
            "headline": article.get("title", "Automotive software update"),
            "summary": summary[:900],
            "why_it_matters": (
                f"This is relevant to {category.lower()} and helps connect traditional "
                "model-based VCU development with current automotive software practices."
            ),
            "key_concepts": concepts[:4],
            "interview_questions": [
                f"How would you explain the role of {concepts[0]} in a modern vehicle architecture?",
                f"What trade-offs would you consider when introducing {concepts[1]} into an EV VCU program?",
            ],
            "next_step": f"Review the fundamentals of {concepts[0]} and relate them to your current VCU workflow.",
            "category": category,
            "source_title": article.get("title", ""),
            "source_url": article.get("url", ""),
            "source": article.get("source", "Unknown"),
            "published": article.get("published", ""),
            "relevance_score": article.get("relevance_score", 0),
            "generation_mode": "template",
        }
