from __future__ import annotations

import os
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

SERVICE_VERSION = "1.0.0-rc3"
RESEARCH_MODE = "RESEARCH_ONLY"
LATEST_COMPLETED_EXPERIMENT = "v0.50"
LATEST_COMPLETED_DECISION = "V50_NONOVERLAP_FAILURE_SUPPORTED"
NEXT_RESEARCH_QUESTION = "v0.51 prospective overlap-conflict arbitration"
KRAKEN_STATE = "SEALED"
CANONICAL_V50_RUN = 34707823108
CANONICAL_V50_HEAD = "1dd0b1fe506fc51ceec4ff8934b77090f86b6cc2"
CANONICAL_V50_ARTIFACT = 10302830689
CANONICAL_V50_DIGEST = "sha256:da5813a8c031f9da6cc940fda942efc846ca536dbd952f4930584c30732373e9"


def _truthy(name: str) -> bool:
    return os.getenv(name, "false").strip().lower() in {"1", "true", "yes", "on"}


if any(
    _truthy(name)
    for name in (
        "LIVE_EXECUTION",
        "PAPER_EXECUTION",
        "BOT_FORWARD_PAPER_ENABLED",
        "BOT_PAPER_EXECUTION_ENABLED",
    )
):
    raise RuntimeError(
        "Execution firewall violation: LIVE/PAPER/forward-paper flags must remain false."
    )

app = FastAPI(
    title="Modular Crypto Trading Bot — Thesis Research API",
    version=SERVICE_VERSION,
    description=(
        "Fail-closed thesis research/monitoring shell. No exchange-order or paper-execution "
        "endpoint is enabled. Scientific implementation remains in the private thesis repository."
    ),
)


def _status() -> dict:
    return {
        "principle": "Evidence Before Opinion",
        "version": SERVICE_VERSION,
        "mode": RESEARCH_MODE,
        "latest_completed_experiment": LATEST_COMPLETED_EXPERIMENT,
        "latest_completed_decision": LATEST_COMPLETED_DECISION,
        "next_research_question": NEXT_RESEARCH_QUESTION,
        "development_venues": ["coinex", "okx", "kucoin"],
        "reserved_holdout": "kraken",
        "kraken_holdout": KRAKEN_STATE,
        "paper_execution": False,
        "live_execution": False,
        "candidate_promotion_allowed": False,
        "v50_provenance": {
            "workflow_run": CANONICAL_V50_RUN,
            "scientific_head": CANONICAL_V50_HEAD,
            "artifact_id": CANONICAL_V50_ARTIFACT,
            "artifact_digest": CANONICAL_V50_DIGEST,
        },
        "deployment_role": "public_fail_closed_monitoring_shell",
        "scientific_source": "private_modular_crypto_trading_bot_repository",
        "release_channel": os.getenv("BOT_RELEASE_CHANNEL", "research-v50-fail-closed"),
        "warning": "Service availability is not profitability evidence or execution authorization.",
    }


@app.get("/")
def root() -> dict:
    return {
        "service": "modular-crypto-research-bot",
        "version": SERVICE_VERSION,
        "mode": RESEARCH_MODE,
        "latest_completed_experiment": LATEST_COMPLETED_EXPERIMENT,
        "latest_completed_decision": LATEST_COMPLETED_DECISION,
        "dashboard": "/dashboard",
        "docs": "/docs",
        "health": "/health",
        "paper_execution": False,
        "live_execution": False,
        "kraken_holdout": KRAKEN_STATE,
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "modular-crypto-research-bot",
        "version": SERVICE_VERSION,
        "execution_mode": RESEARCH_MODE,
        "latest_completed_experiment": LATEST_COMPLETED_EXPERIMENT,
        "paper_execution": False,
        "live_execution": False,
        "kraken_holdout": KRAKEN_STATE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/research/status")
def research_status() -> dict:
    return _status()


@app.get("/research/latest")
def research_latest() -> dict:
    return {
        "experiment": LATEST_COMPLETED_EXPERIMENT,
        "decision": LATEST_COMPLETED_DECISION,
        "finding": (
            "The frozen earliest-first non-overlap stage satisfied the preregistered "
            "broad-harm attribution rule in v0.50. No alternative arbitration rule is validated yet."
        ),
        "next_question": NEXT_RESEARCH_QUESTION,
        "candidate_promotion_allowed": False,
        "kraken_touched": False,
        "paper_execution": False,
        "live_execution": False,
    }


@app.post("/decision/evaluate")
def decision_locked(payload: dict) -> dict:
    del payload
    raise HTTPException(
        status_code=423,
        detail="Decision/execution endpoint is locked by thesis governance; research-only deployment.",
    )


@app.get("/paper/status")
def paper_status() -> dict:
    return {
        "status": "DISABLED_BY_SCIENTIFIC_GATE",
        "paper_execution_enabled": False,
        "live_execution": False,
        "kraken_holdout": KRAKEN_STATE,
        "required_next_step": NEXT_RESEARCH_QUESTION,
    }


@app.post("/paper/run-once")
def paper_locked() -> dict:
    raise HTTPException(
        status_code=423,
        detail="PAPER execution is disabled by the current scientific gate.",
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    return """<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Thesis Crypto Research Bot</title><style>body{font-family:system-ui;margin:0;background:#f5f7fa;color:#17202a}header{background:#111827;color:#fff;padding:24px 5vw}main{max-width:960px;margin:24px auto;padding:0 20px}.card{background:#fff;border:1px solid #dfe5ec;border-radius:12px;padding:18px;margin:14px 0}.warn{background:#fff7ed;border-left:4px solid #f59e0b;padding:12px}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style></head><body><header><h1>Modular Crypto Trading Bot — Thesis Research Dashboard</h1><div>v0.50 · Evidence Before Opinion · fail-closed</div></header><main><div class='warn'>Research/monitoring only. LIVE=false · PAPER=false · Kraken SEALED. No exchange-order endpoint is enabled.</div><div class='card'><h2>Canonical status</h2><pre id='status'>loading…</pre></div><div class='card'><a href='/docs'>API docs</a> · <a href='/health'>Health</a></div></main><script>fetch('/research/status').then(r=>r.json()).then(x=>status.textContent=JSON.stringify(x,null,2))</script></body></html>"""
