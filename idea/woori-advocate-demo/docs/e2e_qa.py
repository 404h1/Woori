"""
Woori Advocate E2E QA.

요구: 서버 기동 (uvicorn main:app --port 8765, WOORI_DEMO_MODE=cache 권장)

검증 항목:
1. GET  /                         → HTML (200)
2. GET  /static/styles.css        → CSS (200)
3. GET  /static/app.js            → JS (200)
4. GET  /.well-known/agent.json   → OCP Agent Card (3 skills)
5. GET  /api/providers/status     → 2 providers
6. POST /api/review               → seller + advocate + Z3 + moderator + audit
7. POST /api/fds/check            → BLOCK + 4 signals + family consent
8. GET  /api/audit/recent         → ≥2 entries (review + fds)

실패 시 exit code 1.
"""
from __future__ import annotations

import json
import sys
import time
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:8765"


def get(path: str) -> tuple[int, str]:
    with urlopen(BASE + path) as resp:
        return resp.status, resp.read().decode("utf-8", errors="replace")


def post(path: str, body: dict) -> tuple[int, dict]:
    req = Request(
        BASE + path,
        data=json.dumps(body).encode("utf-8"),
        headers={"content-type": "application/json"},
        method="POST",
    )
    with urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def assert_(cond: bool, msg: str) -> None:
    if not cond:
        print(f"  ✗ FAIL: {msg}")
        sys.exit(1)
    print(f"  ✓ {msg}")


def main() -> None:
    print(f"E2E QA — {BASE}\n")

    # 1) HTML root
    print("[1] GET /")
    code, body = get("/")
    assert_(code == 200, f"status 200 (got {code})")
    assert_("Woori Advocate" in body, "HTML contains brand")
    assert_("split-view" in body, "HTML contains split-view")

    # 2-3) static
    print("[2] GET /static/styles.css")
    code, body = get("/static/styles.css")
    assert_(code == 200, f"status 200 (got {code})")
    assert_("--woori-blue" in body, "CSS contains brand color var")

    print("[3] GET /static/app.js")
    code, body = get("/static/app.js")
    assert_(code == 200, f"status 200 (got {code})")
    assert_("loadProviderStatus" in body, "JS contains provider status hook")

    # 4) Agent Card
    print("[4] GET /.well-known/agent.json")
    code, body = get("/.well-known/agent.json")
    assert_(code == 200, f"status 200 (got {code})")
    card = json.loads(body)
    assert_(card.get("ocp_version") == "1.0-poc", "ocp_version present")
    assert_(len(card["agent"]["skills"]) == 3, "3 skills declared")

    # 5) providers status
    print("[5] GET /api/providers/status")
    code, body = get("/api/providers/status")
    assert_(code == 200, f"status 200 (got {code})")
    ps = json.loads(body)
    assert_("anthropic" in ps and "openai" in ps, "seller/advocate providers reported")
    assert_(ps["anthropic"]["preferred_path"] in ("api", "cli", "mock"),
            f"anthropic path = {ps['anthropic']['preferred_path']}")

    # 6) review
    print("[6] POST /api/review")
    code, data = post("/api/review", {})
    assert_(code == 200, f"status 200 (got {code})")
    assert_(data["customer"]["name"] == "박영희", "customer = 박영희")
    assert_(data["customer"]["age"] == 75, "age = 75")
    assert_(data["customer"]["senior_mode"] is True, "senior_mode auto-on")
    assert_(len(data["advocate"]["items"]) == 5, "advocate 5 items")
    assert_(data["formal_proof"]["all_passed"] is True, "Z3 SMT passed")
    assert_(data["moderator"]["items_verified"] == 5, "moderator 5/5 verified")
    assert_("trace_id" in data["audit"], "audit trace_id present")
    seller_b = data["seller"]["backend"]
    advocate_b = data["advocate"]["backend"]
    print(f"     seller backend  : {seller_b}")
    print(f"     advocate backend: {advocate_b}")

    # 7) FDS
    print("[7] POST /api/fds/check")
    code, data = post("/api/fds/check", {})
    assert_(code == 200, f"status 200 (got {code})")
    assert_(data["fds"]["recommendation"] == "BLOCK", "FDS BLOCK")
    assert_(data["fds"]["risk_score"] >= 0.7, f"risk_score = {data['fds']['risk_score']}")
    assert_(len(data["fds"]["triggered_signals"]) >= 4, "≥4 signals")
    assert_(data["family_consent"]["required"] is True, "family consent required")

    # 8) audit trail
    print("[8] GET /api/audit/recent")
    code, body = get("/api/audit/recent")
    assert_(code == 200, f"status 200 (got {code})")
    audits = json.loads(body)["audits"]
    assert_(len(audits) >= 2, f"≥2 audit entries (got {len(audits)})")

    print("\n✓ ALL E2E CHECKS PASSED")


if __name__ == "__main__":
    main()
