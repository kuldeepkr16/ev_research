"""Generate one technology deep dive and one industry-update brief."""

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
    "Open Automotive Software": ["SDV", "open-source middleware", "vehicle APIs", "platform architecture"],
}


class ResearchGenerator:
    def __init__(self) -> None:
        self.provider = get_ai_provider()

    def generate_technology(self, topic: dict[str, Any]) -> dict[str, Any]:
        base = self._technology_template(topic)
        if isinstance(self.provider, TemplateProvider):
            return base

        prompt = f"""
{LEARNING_FOCUS}

Create a practical technology deep dive using ONLY the curated facts below.
The reader wants to compare modern/open-source tooling with their current
MATLAB/Simulink, CANalyzer/CANoe and INCA-oriented workflow.

TECHNOLOGY: {topic['name']}
CATEGORY: {topic['category']}
CURRENT STACK: {topic['current_stack']}
RELATIONSHIP: {topic['relationship']}
CURATED OVERVIEW: {topic['overview']}
KNOWN LIMITATIONS: {topic['limitations']}
LEARNING GOALS: {', '.join(topic['learning_goals'])}
OFFICIAL SOURCE: {topic['source_url']}

Be explicit about functional overlap and gaps. Do not claim that this technology
fully replaces the current stack unless the supplied relationship says so.
Do not invent company adoption claims.

Return valid JSON only:
{{
  "headline": "clear comparison-oriented title",
  "summary": "3-5 sentences explaining what it is and where it fits",
  "why_it_matters": "2-3 sentences for a VCU/model-based developer",
  "comparison_note": "specific explanation of what it replaces, complements, or does not cover",
  "practical_example": "one small hands-on exercise or realistic workflow",
  "key_concepts": ["3-5 concepts"],
  "interview_questions": ["2 realistic interview questions"],
  "next_step": "one concrete next learning step"
}}
"""
        parsed = self._generate_json(prompt)
        if not parsed:
            return base

        self._merge_text_fields(
            base,
            parsed,
            ("headline", "summary", "why_it_matters", "comparison_note", "practical_example", "next_step"),
        )
        self._merge_list_fields(base, parsed, ("key_concepts", "interview_questions"))
        base["generation_mode"] = "ai"
        return base

    def generate_industry(self, article: dict[str, Any]) -> dict[str, Any]:
        base = self._industry_template(article)
        if isinstance(self.provider, TemplateProvider):
            return base

        prompt = f"""
{LEARNING_FOCUS}

Create a factual engineering-focused brief from the recent source metadata below.
Do not invent facts unsupported by the title/description. Ignore commercial hype
and focus on architecture, controls, software, validation, diagnostics, tooling,
standards, or EV powertrain engineering implications.

SOURCE TITLE: {article.get('title', '')}
SOURCE DESCRIPTION: {article.get('description', '')[:1800]}
SOURCE/PUBLISHER: {article.get('source', '')}
CATEGORY: {article.get('category', '')}

Return valid JSON only:
{{
  "headline": "short engineering-focused headline",
  "summary": "2-4 concise sentences about what the source reports",
  "why_it_matters": "2-3 sentences connecting it to VCU/EV embedded work",
  "key_concepts": ["3-5 concepts or technologies worth learning"],
  "interview_questions": ["2 realistic interview questions"],
  "next_step": "one concrete topic or exercise to study next"
}}
"""
        parsed = self._generate_json(prompt)
        if not parsed:
            return base

        self._merge_text_fields(base, parsed, ("headline", "summary", "why_it_matters", "next_step"))
        self._merge_list_fields(base, parsed, ("key_concepts", "interview_questions"))
        base["generation_mode"] = "ai"
        return base

    def _generate_json(self, prompt: str) -> dict[str, Any] | None:
        system = (
            "You are an automotive embedded-software research assistant. "
            "Be technically precise, conservative with claims, and return JSON only."
        )
        try:
            response = self.provider.generate(prompt, system)
            return parse_json_response(response)
        except Exception as exc:
            print(f"AI generation warning: {type(exc).__name__}: {exc}")
            return None

    @staticmethod
    def _merge_text_fields(base: dict[str, Any], parsed: dict[str, Any], fields: tuple[str, ...]) -> None:
        for field in fields:
            value = parsed.get(field)
            if isinstance(value, str) and value.strip():
                base[field] = value.strip()

    @staticmethod
    def _merge_list_fields(base: dict[str, Any], parsed: dict[str, Any], fields: tuple[str, ...]) -> None:
        for field in fields:
            value = parsed.get(field)
            if isinstance(value, list):
                cleaned = [str(item).strip() for item in value if str(item).strip()]
                if cleaned:
                    base[field] = cleaned[:5]

    @staticmethod
    def _technology_template(topic: dict[str, Any]) -> dict[str, Any]:
        goals = topic["learning_goals"]
        return {
            "id": f"tech-{topic['id']}",
            "content_type": "technology",
            "tool_id": topic["id"],
            "tool_name": topic["name"],
            "headline": f"{topic['name']}: where it fits in your current stack",
            "summary": topic["overview"],
            "why_it_matters": (
                "Understanding the exact overlap lets a VCU engineer separate capabilities "
                "that can move to open tooling from functions that still depend on mature "
                "automotive commercial ecosystems."
            ),
            "current_stack": topic["current_stack"],
            "relationship": topic["relationship"],
            "comparison_note": f"{topic['overview']} {topic['limitations']}",
            "limitations": topic["limitations"],
            "practical_example": (
                f"Build a small proof of concept around {goals[0]} and document which part "
                "of your current workflow it can reproduce."
            ),
            "key_concepts": goals[:4],
            "interview_questions": [
                f"Where would {topic['name']} fit in an EV VCU development workflow?",
                f"What would {topic['name']} not replace from your current proprietary toolchain?",
            ],
            "next_step": f"Start with {goals[0]} and reproduce one small task from your current workflow.",
            "category": topic["category"],
            "source_title": f"{topic['name']} official documentation",
            "source_url": topic["source_url"],
            "source": topic["official_source"],
            "published": "",
            "relevance_score": 10,
            "generation_mode": "template",
        }

    @staticmethod
    def _industry_template(article: dict[str, Any]) -> dict[str, Any]:
        category = article.get("category", "Automotive Software")
        concepts = CATEGORY_CONCEPTS.get(
            category,
            ["embedded software", "VCU", "automotive systems"],
        )
        description = article.get("description", "").strip()
        summary = description or (
            "This source covers a recent engineering development relevant to automotive "
            "software. Open the source article for the full context."
        )
        return {
            "id": article.get("id", ""),
            "content_type": "industry",
            "headline": article.get("title", "Automotive engineering update"),
            "summary": summary[:900],
            "why_it_matters": (
                f"This update is relevant to {category.lower()} and helps connect daily VCU "
                "development with changes in the wider automotive engineering ecosystem."
            ),
            "key_concepts": concepts[:4],
            "interview_questions": [
                f"How would you explain the role of {concepts[0]} in a modern vehicle architecture?",
                f"What trade-offs would you consider when introducing {concepts[1]} into an EV VCU program?",
            ],
            "next_step": f"Review {concepts[0]} and connect it to your current VCU workflow.",
            "category": category,
            "source_title": article.get("title", ""),
            "source_url": article.get("url", ""),
            "source": article.get("source", "Unknown"),
            "published": article.get("published", ""),
            "relevance_score": article.get("relevance_score", 0),
            "generation_mode": "template",
        }
