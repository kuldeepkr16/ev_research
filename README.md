# EV / VCU Industry Research Dashboard

A daily research and interview-preparation dashboard for Model-Based Developers
working on EV powertrain and Vehicle Control Unit (VCU) software.

Each run finds recent automotive software sources and creates exactly **two**
learning briefs. Every brief keeps the original source article link and adds:

- a concise summary;
- why the development matters for VCU / EV embedded work;
- concepts and technologies worth learning;
- realistic interview questions;
- one concrete next learning step.

The research scope includes automotive Ethernet, CAN FD/CAN XL, SOME/IP,
AUTOSAR, software-defined and zonal vehicle architecture, diagnostics/DoIP,
OTA, ISO 26262, Automotive SPICE, SIL/HIL/virtual ECUs, EV powertrain controls,
automotive cybersecurity, calibration and modern development tooling.

## Architecture

```text
RSS/news sources
      ↓
Python source collection + ranking
      ↓
AI-assisted learning brief generation
      ↓
output/ev_research_*.json
      ↓
scripts/build_frontend_data.py
      ↓
frontend/data/{latest.json,history.json,runs/}
      ↓
Static GitHub Pages dashboard
```

The dashboard is completely static. Review status is stored in the browser's
`localStorage`; no backend is required.

## Run locally

Use Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py --count 2
python scripts/build_frontend_data.py
python -m http.server 8000 -d frontend
```

Open `http://localhost:8000`.

## Environment variables

The default provider is Groq:

```text
AI_PROVIDER=groq
GROQ_API_KEY=...
GROQ_MODEL=openai/gpt-oss-120b
```

Gemini and Ollama are also supported through the variables shown in
`.env.example`. If no cloud key is configured, the generator falls back to a
deterministic source-based brief so credentials are never required to render the
dashboard.

Never commit `.env` or API keys.

## Daily GitHub Actions automation

`.github/workflows/daily-run.yml` runs every day at **08:00 IST** and can also
be started manually with **Actions → Daily EV Research → Run workflow**.

The workflow:

1. checks out the repository;
2. installs Python dependencies;
3. generates exactly two briefs;
4. builds `latest.json`, `history.json` and the versioned run;
5. verifies both briefs contain source links;
6. commits the generated dashboard history;
7. deploys `frontend/` with GitHub Pages.

## Repository secret

In GitHub, open **Settings → Secrets and variables → Actions → New repository
secret** and add:

`GROQ_API_KEY`

Use the same key you use locally. Do not put the key into the workflow YAML.

## Enable GitHub Pages

Open **Settings → Pages** and set **Source** to **GitHub Actions**. The
`actions/deploy-pages` step in the workflow will publish the `frontend/`
directory.

## Project structure

```text
.
├── main.py
├── config.py
├── ai_providers.py
├── news_fetcher.py
├── research_generator.py
├── requirements.txt
├── README.md
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── data/
│       ├── latest.json
│       ├── history.json
│       └── runs/
├── scripts/
│   └── build_frontend_data.py
└── .github/
    └── workflows/
        └── daily-run.yml
```