"""Generate one technology deep dive and one recent EV/automotive update."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from rich.console import Console
from rich.panel import Panel

from config import AI_PROVIDER, ARTICLES_PER_RUN, OUTPUT_DIR
from news_fetcher import AutomotiveNewsFetcher, select_industry_update
from research_generator import ResearchGenerator
from technology_catalog import select_next_technology


ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / OUTPUT_DIR
RUNS_PATH = ROOT / "frontend" / "data" / "runs"
console = Console()


def load_seen_state() -> tuple[set[str], set[str]]:
    seen_technologies: set[str] = set()
    seen_industry: set[str] = set()
    paths = list(RUNS_PATH.glob("ev_research_*.json")) if RUNS_PATH.exists() else []
    if OUTPUT_PATH.exists():
        paths.extend(OUTPUT_PATH.glob("ev_research_*.json"))

    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        for article in data.get("articles", []):
            if article.get("content_type") == "technology":
                if article.get("tool_id"):
                    seen_technologies.add(article["tool_id"])
            elif article.get("id"):
                seen_industry.add(article["id"])

    return seen_technologies, seen_industry


def save_run(articles: list[dict]) -> Path:
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    path = OUTPUT_PATH / f"ev_research_{now.strftime('%Y%m%d_%H%M%S')}.json"
    payload = {
        "generated_at": now.isoformat(),
        "ai_provider": AI_PROVIDER,
        "article_count": len(articles),
        "stream_counts": {"technology": 1, "industry": 1},
        "articles": articles,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate daily EV/VCU learning briefs")
    parser.add_argument("--count", type=int, default=ARTICLES_PER_RUN)
    parser.add_argument("--no-save", action="store_true")
    args = parser.parse_args()
    if args.count != 2:
        raise SystemExit("Expected exactly 2 briefs: 1 technology + 1 industry update.")

    console.print(Panel.fit("EV / VCU Daily Learning", style="bold cyan"))
    seen_technologies, seen_industry = load_seen_state()
    technology = select_next_technology(seen_technologies)

    news_sources = AutomotiveNewsFetcher().fetch()
    industry_source = select_industry_update(news_sources, seen_industry)
    if industry_source is None:
        raise SystemExit("No usable recent industry source found. No partial run was saved.")

    generator = ResearchGenerator()
    articles = [
        generator.generate_technology(technology),
        generator.generate_industry(industry_source),
    ]

    types = [article.get("content_type") for article in articles]
    if types.count("technology") != 1 or types.count("industry") != 1:
        raise SystemExit("Run must contain exactly one technology brief and one industry brief.")
    if not all(article.get("source_url") for article in articles):
        raise SystemExit("Every brief must contain a source link.")

    if args.no_save:
        console.print_json(data={"articles": articles})
        return

    path = save_run(articles)
    console.print(f"[green]Saved 2 briefs to {path}[/green]")


if __name__ == "__main__":
    main()
