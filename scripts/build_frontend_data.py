"""Publish generated EV research runs as static GitHub Pages JSON."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
DATA_DIR = ROOT / "frontend" / "data"
RUNS_DIR = DATA_DIR / "runs"


def read_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def valid_run(data: dict) -> bool:
    articles = data.get("articles")
    return isinstance(articles, list) and len(articles) > 0


def main() -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_DIR.exists():
        for source in sorted(OUTPUT_DIR.glob("ev_research_*.json")):
            data = read_json(source)
            if data and valid_run(data):
                shutil.copy2(source, RUNS_DIR / source.name)

    runs = []
    for path in RUNS_DIR.glob("ev_research_*.json"):
        data = read_json(path)
        if not data or not valid_run(data):
            continue
        articles = data["articles"]
        categories = sorted({item.get("category", "Other") for item in articles})
        sources = sorted({item.get("source", "Unknown") for item in articles})
        runs.append(
            {
                "generated_at": data.get("generated_at", ""),
                "ai_provider": data.get("ai_provider", "unknown"),
                "article_count": len(articles),
                "categories": categories,
                "sources": sources,
                "path": f"data/runs/{path.name}",
                "filename": path.name,
            }
        )

    runs.sort(key=lambda item: item["generated_at"], reverse=True)
    history = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "runs": runs,
    }
    (DATA_DIR / "history.json").write_text(
        json.dumps(history, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if runs:
        latest = read_json(ROOT / "frontend" / runs[0]["path"])
    else:
        latest = {
            "generated_at": "",
            "ai_provider": "unknown",
            "article_count": 0,
            "articles": [],
        }
    (DATA_DIR / "latest.json").write_text(
        json.dumps(latest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Dashboard data ready: {len(runs)} historical run(s)")


if __name__ == "__main__":
    main()
