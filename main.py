"""Generate exactly two current EV/VCU learning briefs per run."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from rich.console import Console
from rich.panel import Panel

from config import AI_PROVIDER, ARTICLES_PER_RUN, OUTPUT_DIR
from news_fetcher import AutomotiveNewsFetcher, select_articles
from research_generator import ResearchGenerator


ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / OUTPUT_DIR
RUNS_PATH = ROOT / "frontend" / "data" / "runs"
console = Console()


def load_seen_ids() -> set[str]:
    seen: set[str] = set()
    paths = list(RUNS_PATH.glob("ev_research_*.json")) if RUNS_PATH.exists() else []
    if OUTPUT_PATH.exists():
        paths.extend(OUTPUT_PATH.glob("ev_research_*.json"))
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for article in data.get("articles", []):
            article_id = article.get("id")
            if article_id:
                seen.add(article_id)
    return seen


def save_run(articles: list[dict]) -> Path:
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    filename = f"ev_research_{now.strftime('%Y%m%d_%H%M%S')}.json"
    path = OUTPUT_PATH / filename
    payload = {
        "generated_at": now.isoformat(),
        "ai_provider": AI_PROVIDER,
        "article_count": len(articles),
        "articles": articles,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate EV/VCU industry learning briefs")
    parser.add_argument("--count", type=int, default=ARTICLES_PER_RUN)
    parser.add_argument("--no-save", action="store_true")
    args = parser.parse_args()

    if args.count < 1:
        raise SystemExit("--count must be at least 1")

    console.print(Panel.fit("EV / VCU Industry Research", style="bold cyan"))
    console.print(f"Target: [bold]{args.count}[/bold] briefs · AI provider: [bold]{AI_PROVIDER}[/bold]")

    sources = AutomotiveNewsFetcher().fetch()
    console.print(f"Found {len(sources)} unique recent sources")
    selected = select_articles(sources, args.count, load_seen_ids())
    if len(selected) < args.count:
        raise SystemExit(
            f"Only {len(selected)} usable sources found; expected {args.count}. "
            "No partial run was saved."
        )

    generator = ResearchGenerator()
    briefs = []
    for source in selected:
        console.print(f"Generating: {source['title'][:80]}")
        briefs.append(generator.generate(source))

    if len(briefs) != args.count:
        raise SystemExit(f"Generated {len(briefs)} briefs; expected {args.count}.")

    if args.no_save:
        console.print_json(data={"articles": briefs})
        return

    path = save_run(briefs)
    console.print(f"[green]Saved {len(briefs)} briefs to {path}[/green]")


if __name__ == "__main__":
    main()
