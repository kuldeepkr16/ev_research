# EV / VCU Daily Learning Dashboard

A daily learning and interview-preparation dashboard for Model-Based Developers working on EV powertrain and Vehicle Control Unit software.

Every run creates exactly **two different briefs**:

1. **Technology Deep Dive** — one curated open-source or lower-cost technology, explained against the current MATLAB/Simulink, CANalyzer/CANoe, INCA, and proprietary embedded-tool workflow.
2. **EV / Automotive Industry Update** — one recent engineering-relevant source covering vehicle software, EV powertrain, architecture, communications, testing, diagnostics, safety, cybersecurity, or open automotive platforms.

Every card includes a source link. Technology cards use the project's official documentation; industry cards keep the original article link.

## Technology roadmap

The technology stream is deliberately **not news-driven**. It progresses through a curated roadmap and avoids repeating a tool until the roadmap has been covered.

Topics include:

- OpenModelica and Scilab/Xcos
- Python Control Systems Library
- CasADi and acados
- FMI/FMU
- SocketCAN and can-utils
- python-can and cantools
- Wireshark for Automotive Ethernet
- COVESA vsomeip and Vehicle Signal Specification
- Eclipse iceoryx, Zenoh, KUKSA, S-CORE, and Cyclone DDS
- Zephyr and Eclipse ThreadX
- QEMU and virtual-ECU concepts
- CMake with GCC/Clang
- pytest for ECU test automation
- open UDS/DoIP tooling
- pyXCP and asammdf

Technology briefs explicitly show:

- the current proprietary stack/function being compared;
- whether the technology is an alternative, complement, or partial replacement;
- what it can cover;
- what it does **not** replace;
- a practical learning exercise;
- interview questions and a next step.

This distinction matters because there is no single open-source drop-in replacement for the complete MATLAB/Simulink, CANoe, or INCA ecosystems.

## Industry update stream

Only the second daily brief searches recent sources. Queries prioritize engineering developments around:

- CAN FD/CAN XL, Automotive Ethernet, SOME/IP, and zonal architecture;
- AUTOSAR and software-defined vehicles;
- UDS, DoIP, OTA, and diagnostics;
- ISO 26262 and Automotive SPICE;
- MIL/SIL/HIL and virtual ECUs;
- VCU, BMS, inverter, and EV powertrain software;
- ISO/SAE 21434 and automotive cybersecurity;
- open automotive software such as Eclipse SDV and COVESA.

Common sales, stock-price, discount, booking, and vehicle-review noise is filtered out.

## Architecture

~~~text
Curated technology roadmap ──┐
                             ├─> Python brief generation
Recent engineering sources ──┘
                                      ↓
                           output/ev_research_*.json
                                      ↓
                       scripts/build_frontend_data.py
                                      ↓
              frontend/data/{latest.json,history.json,runs/}
                                      ↓
                         Static GitHub Pages dashboard
~~~

The dashboard is completely static. Review status is stored in browser localStorage; no backend server is required.

## Run locally

Use Python 3.11+.

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py --count 2
python scripts/build_frontend_data.py
python -m http.server 8000 -d frontend
~~~

Then open http://localhost:8000.

## Environment variables

The default AI provider is Groq:

~~~text
AI_PROVIDER=groq
GROQ_API_KEY=...
GROQ_MODEL=openai/gpt-oss-120b
~~~

Gemini and Ollama are also supported through the variables in .env.example. If no cloud key is configured, the generator uses deterministic fallback text.

Never commit .env or API keys.

## Daily GitHub Actions automation

.github/workflows/daily-run.yml runs every day at **05:00 IST** and can also be started manually from **Actions → Daily EV Research → Run workflow**.

The workflow:

1. checks out the repository;
2. installs Python dependencies;
3. creates exactly two briefs;
4. updates latest.json, history.json, and the versioned run;
5. verifies both briefs have source links;
6. commits generated dashboard history;
7. deploys frontend/ with GitHub Pages.

The generator itself additionally verifies the run contains exactly **one technology brief and one industry brief**.

## Repository secret

In GitHub open **Settings → Secrets and variables → Actions → New repository secret** and add:

**GROQ_API_KEY**

Use the same key you use locally. Do not put the key in the workflow YAML or repository files.

## Enable GitHub Pages

Open **Settings → Pages** and set **Source** to **GitHub Actions**.

## Project structure

~~~text
.
├── main.py
├── config.py
├── technology_catalog.py
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
~~~
