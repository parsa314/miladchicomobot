from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_is_fail_closed_v50():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == "1.0.0-rc3"
    assert body["execution_mode"] == "RESEARCH_ONLY"
    assert body["latest_completed_experiment"] == "v0.50"
    assert body["paper_execution"] is False
    assert body["live_execution"] is False
    assert body["kraken_holdout"] == "SEALED"


def test_canonical_status_is_v50():
    body = client.get("/research/status").json()
    assert body["latest_completed_decision"] == "V50_NONOVERLAP_FAILURE_SUPPORTED"
    assert body["v50_provenance"]["workflow_run"] == 34707823108
    assert body["v50_provenance"]["artifact_id"] == 10302830689
    assert body["candidate_promotion_allowed"] is False


def test_execution_routes_are_locked():
    assert client.post("/decision/evaluate", json={}).status_code == 423
    assert client.post("/paper/run-once").status_code == 423
