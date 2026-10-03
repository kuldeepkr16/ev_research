"""Configuration for the EV / VCU industry research dashboard."""

from __future__ import annotations

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv


load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "groq").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

OUTPUT_DIR = "output"
ARTICLES_PER_RUN = 2
LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", "7"))

TOPIC_QUERIES = [
    {
        "category": "Communication",
        "query": "automotive Ethernet SOME/IP CAN XL zonal architecture",
        "keywords": ["ethernet", "some/ip", "someip", "can xl", "can fd", "tsn"],
    },
    {
        "category": "Software Architecture",
        "query": "software defined vehicle AUTOSAR adaptive automotive architecture",
        "keywords": ["software-defined vehicle", "sdv", "autosar", "adaptive", "zonal"],
    },
    {
        "category": "Diagnostics & OTA",
        "query": "automotive diagnostics UDS DoIP OTA vehicle software",
        "keywords": ["uds", "doip", "diagnostic", "ota", "over-the-air"],
    },
    {
        "category": "Safety & Process",
        "query": "ISO 26262 Automotive SPICE functional safety EV software",
        "keywords": ["iso 26262", "aspice", "automotive spice", "functional safety"],
    },
    {
        "category": "Testing & Validation",
        "query": "automotive SIL HIL virtual ECU testing model based development",
        "keywords": ["sil", "hil", "virtual ecu", "simulation", "model-based"],
    },
    {
        "category": "EV Powertrain",
        "query": "electric vehicle VCU torque control battery powertrain software",
        "keywords": ["vcu", "torque", "powertrain", "battery", "inverter", "ev"],
    },
    {
        "category": "Cybersecurity",
        "query": "automotive cybersecurity ISO 21434 UNECE R155 vehicle software",
        "keywords": ["iso 21434", "r155", "cybersecurity", "secure boot"],
    },
    {
        "category": "Development Tools",
        "query": "automotive embedded software CI CD calibration CANoe INCA MATLAB Simulink",
        "keywords": ["canoe", "canalyzer", "inca", "simulink", "ci/cd", "calibration"],
    },
]

LEARNING_FOCUS = """
The reader is a Model-Based Developer working on Vehicle Control Unit software
for EV powertrains. They already use MATLAB/Simulink, CAN, CANalyzer and INCA.
The brief should help them learn current global automotive software practices
and prepare for interviews in EV powertrain, VCU and embedded automotive roles.
"""


def google_news_feed(query: str, lookback_days: int = LOOKBACK_DAYS) -> str:
    search = quote_plus(f"{query} when:{lookback_days}d")
    return (
        "https://news.google.com/rss/search?"
        f"q={search}&hl=en-US&gl=US&ceid=US:en"
    )
