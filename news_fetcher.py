"""Fetch one recent engineering-relevant EV/automotive industry update."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any

import feedparser
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from config import NEWS_NOISE_TERMS, TOPIC_QUERIES, google_news_feed


def _clean_html(value: str) -> str:
    if not value:
        return ""
    soup = BeautifulSoup(value, "html.parser")
    return " ".join(soup.get_text(" ", strip=True).split())


def _parse_date(value: str) -> datetime:
    try:
        parsed = date_parser.parse(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError, OverflowError):
        return datetime.now(timezone.utc)


def _normalized_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def _article_id(title: str, url: str) -> str:
    raw = f"{title}|{url}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:16]


def _is_noise(title: str, summary: str) -> bool:
    haystack = f"{title} {summary}".lower()
    return any(term in haystack for term in NEWS_NOISE_TERMS)


class AutomotiveNewsFetcher:
    def fetch(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for topic in TOPIC_QUERIES:
            feed = feedparser.parse(google_news_feed(topic["query"]))
            if getattr(feed, "bozo", False) and not feed.entries:
                error = getattr(feed, "bozo_exception", "unknown RSS error")
                print(f"RSS warning for {topic['category']}: {error}")
                continue

            for entry in feed.entries[:12]:
                title = _clean_html(entry.get("title", ""))
                url = entry.get("link", "")
                if not title or not url:
                    continue

                summary = _clean_html(entry.get("summary", entry.get("description", "")))
                if _is_noise(title, summary):
                    continue

                published_text = entry.get("published", entry.get("updated", ""))
                published_dt = _parse_date(published_text)
                source_obj = entry.get("source") or {}
                source_name = (
                    source_obj.get("title", "")
                    if isinstance(source_obj, dict)
                    else getattr(source_obj, "title", "")
                )
                haystack = f"{title} {summary}".lower()
                keyword_hits = sum(1 for keyword in topic["keywords"] if keyword in haystack)
                items.append(
                    {
                        "id": _article_id(title, url),
                        "title": title,
                        "description": summary,
                        "url": url,
                        "source": source_name or "Google News",
                        "published": published_dt.isoformat(),
                        "category": topic["category"],
                        "relevance_score": 1 + keyword_hits,
                    }
                )

        return self._dedupe_and_rank(items)

    @staticmethod
    def _dedupe_and_rank(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        deduped: dict[str, dict[str, Any]] = {}
        for item in items:
            key = _normalized_title(item["title"])
            current = deduped.get(key)
            if current is None or item["relevance_score"] > current["relevance_score"]:
                deduped[key] = item

        return sorted(
            deduped.values(),
            key=lambda item: (item["relevance_score"], item["published"]),
            reverse=True,
        )


def select_industry_update(
    articles: list[dict[str, Any]],
    seen_ids: set[str] | None = None,
) -> dict[str, Any] | None:
    """Prefer the highest-ranked unseen engineering update."""
    seen_ids = seen_ids or set()
    for article in articles:
        if article["id"] not in seen_ids:
            return article
    return articles[0] if articles else None
