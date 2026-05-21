"""
Woori Advocate — FastAPI orchestrator.

엔드포인트:
- GET  /                            → 정적 프론트엔드 (좌우 분할 UI)
- GET  /.well-known/agent.json     → OCP Agent Card
- POST /api/review                  → Seller·Advocate·Moderator·Z3 통합 호출
- POST /api/fds/check               → FDS 평가 + Family Consent
- GET  /api/audit/recent            → 최근 audit trail

실행:
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents import (
    load_customer,
    load_product,
    load_terms_chunks,
    moderate_advocate_items,
    run_mad_debate,
    run_seller_and_advocate,
)
from fds_family import evaluate_fds, request_family_consent
from ocp_audit import append_audit, get_agent_card, read_recent_audits
from providers import report_provider_status
from z3_verifier import verify_seller_output


REPO_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = REPO_ROOT / "frontend"


app = FastAPI(
    title="Woori Advocate",
    version="0.1.0-poc",
    description=(
        "고객 편 AI — Seller(은행 편) vs Advocate(고객 편) 이중 관점 동시 출력. "
        "Iter-0004 grand design 압축 PoC."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────────────────────────────────
# Request/response 모델
# ──────────────────────────────────────────────────────────────────────────

class ReviewRequest(BaseModel):
    customer_id: str = Field(default="park_younghee_75", description="mock 고객 ID")
    product_id: str = Field(default="els_hongkong_h_2026_05", description="mock 상품 ID")


class TransferRequest(BaseModel):
    customer_id: str = Field(default="park_younghee_75")
    amount_krw: int = Field(default=15_000_000)
    recipient_name: str = Field(default="이주민 (자칭 손주)")
    recipient_account_age_days: int = Field(default=3)
    recipient_claimed_relation: str = Field(default="손주")
    recipient_actual_call_history_6m_count: int = Field(default=0)


# ──────────────────────────────────────────────────────────────────────────
# OCP / 정적 라우트
# ──────────────────────────────────────────────────────────────────────────

@app.get("/.well-known/agent.json")
async def agent_card() -> JSONResponse:
    return JSONResponse(get_agent_card())


@app.get("/api/audit/recent")
async def audit_recent(limit: int = 20) -> JSONResponse:
    return JSONResponse({"audits": read_recent_audits(limit=limit)})


@app.get("/api/providers/status")
async def providers_status() -> JSONResponse:
    """각 LLM provider 의 현재 가용 인증 경로 진단 (API key / CLI / mock)."""
    return JSONResponse(report_provider_status())


# 데모 녹화 보조 엔드포인트 (개발용) — html2canvas PNG 데이터 URL 수신
import base64
from pydantic import BaseModel as _BM


class _ScreenshotPayload(_BM):
    name: str
    data_url: str  # "data:image/png;base64,...."


@app.post("/api/_dev/save_screenshot")
async def _save_screenshot(payload: _ScreenshotPayload) -> JSONResponse:
    if "base64," not in payload.data_url:
        raise HTTPException(status_code=400, detail="invalid data URL")
    b64 = payload.data_url.split("base64,", 1)[1]
    raw = base64.b64decode(b64)
    safe_name = Path(payload.name).name  # 경로 분리 방지
    out = REPO_ROOT / "docs" / "demo_recording" / safe_name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    return JSONResponse({"saved": str(out), "bytes": len(raw)})


# ──────────────────────────────────────────────────────────────────────────
# 핵심 엔드포인트
# ──────────────────────────────────────────────────────────────────────────

@app.post("/api/review")
async def review(req: ReviewRequest) -> dict[str, Any]:
    """Seller + Advocate 병렬 호출 → Z3 검증 → Moderator → OCP audit."""
    try:
        customer = load_customer(req.customer_id)
        product = load_product(req.product_id)
        terms_chunks = load_terms_chunks(req.product_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    seller, advocate = await run_seller_and_advocate(customer, product, terms_chunks)

    z3_proof = verify_seller_output(seller.text)
    moderator = moderate_advocate_items(advocate.items, terms_chunks)

    audit_envelope = append_audit(
        customer_id=req.customer_id,
        product_id=req.product_id,
        seller_meta={
            "backend": seller.backend,
            "model_hint": seller.model_hint,
            "char_len": len(seller.text),
        },
        advocate_meta={
            "backend": advocate.backend,
            "model_hint": advocate.model_hint,
            "item_count": len(advocate.items),
        },
        z3_proof=z3_proof,
        moderator=moderator,
    )

    senior_mode = "senior_mode_eligible" in customer["profile"].get(
        "accessibility_flags", []
    )

    return {
        "customer": {
            "name": customer["name"],
            "age": customer["age"],
            "senior_mode": senior_mode,
        },
        "product": {
            "name": product["name"],
            "category": product["category"],
        },
        "seller": {
            "text": seller.text,
            "backend": seller.backend,
            "model_hint": seller.model_hint,
        },
        "advocate": {
            "items": advocate.items,
            "backend": advocate.backend,
            "model_hint": advocate.model_hint,
        },
        "formal_proof": z3_proof,
        "moderator": moderator,
        "audit": {
            "trace_id": audit_envelope["trace_id"],
            "ocp_version": audit_envelope["ocp_version"],
            "digest": audit_envelope["envelope_digest"],
        },
    }


@app.post("/api/review_mad")
async def review_mad(req: ReviewRequest, rounds: int = 2) -> dict[str, Any]:
    """
    MAD (Multi-Agent Debate) 토론 모드 — N 라운드 cross-context embedding.

    Round 1: 독립 호출 (병렬)
    Round 2~N: 각 LLM 이 상대의 직전 출력을 context 에 받아 재작성
    최종: Moderator 가 합의/불일치 JSON 추출

    rounds=2 권장 (2 라운드 + consensus = 약 4~6 LLM 호출).
    """
    try:
        customer = load_customer(req.customer_id)
        product = load_product(req.product_id)
        terms_chunks = load_terms_chunks(req.product_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    history, consensus = await run_mad_debate(
        customer, product, terms_chunks, rounds=rounds,
    )

    # 마지막 라운드 출력으로 Z3 검증
    final_seller_text = history[-1].seller_text
    final_advocate_items = history[-1].advocate_items
    z3_proof = verify_seller_output(final_seller_text)
    moderator = moderate_advocate_items(final_advocate_items, terms_chunks)

    audit_envelope = append_audit(
        customer_id=req.customer_id,
        product_id=req.product_id + f"_mad_r{rounds}",
        seller_meta={"backend": history[-1].seller_backend,
                     "rounds": len(history)},
        advocate_meta={"backend": history[-1].advocate_backend,
                       "item_count": len(final_advocate_items),
                       "rounds": len(history)},
        z3_proof=z3_proof,
        moderator=moderator,
    )

    return {
        "customer": {
            "name": customer["name"],
            "age": customer["age"],
            "senior_mode": "senior_mode_eligible" in customer["profile"].get(
                "accessibility_flags", []),
        },
        "product": {"name": product["name"], "category": product["category"]},
        "debate_rounds": [
            {
                "round": r.round_num,
                "seller": {"text": r.seller_text, "backend": r.seller_backend},
                "advocate": {"items": r.advocate_items, "backend": r.advocate_backend},
            }
            for r in history
        ],
        "consensus": {
            "agreed": consensus.agreed,
            "disagreed": consensus.disagreed,
            "verdict": consensus.verdict,
        },
        "formal_proof": z3_proof,
        "moderator": moderator,
        "audit": {
            "trace_id": audit_envelope["trace_id"],
            "ocp_version": audit_envelope["ocp_version"],
            "digest": audit_envelope["envelope_digest"],
        },
    }


@app.post("/api/fds/check")
async def fds_check(req: TransferRequest) -> dict[str, Any]:
    """통합 시나리오 0 의 송금 단계 — FDS + Family Consent 동시 발동."""
    try:
        customer = load_customer(req.customer_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    transfer = {
        "amount_krw": req.amount_krw,
        "recipient_account_age_days": req.recipient_account_age_days,
        "recipient_claimed_relation": req.recipient_claimed_relation,
        "recipient_actual_call_history_6m_count": req.recipient_actual_call_history_6m_count,
    }
    fds = evaluate_fds(customer, transfer)
    family = request_family_consent(customer, fds)

    audit_envelope = append_audit(
        customer_id=req.customer_id,
        product_id="transfer:" + req.recipient_name,
        seller_meta={"backend": "n/a"},
        advocate_meta={"backend": "n/a"},
        z3_proof={"verifier": "n/a", "all_passed": True, "verified_principles": []},
        moderator={"checker": "n/a"},
        fds={
            "risk_score": fds.risk_score,
            "triggered_signals": fds.triggered_signals,
            "recommendation": fds.recommendation,
        },
        family_consent={
            "required": family.required,
            "contacts_to_verify": family.contacts_to_verify,
            "flow": family.flow,
        },
    )

    return {
        "customer_name": customer["name"],
        "transfer": transfer,
        "fds": {
            "risk_score": fds.risk_score,
            "triggered_signals": fds.triggered_signals,
            "recommendation": fds.recommendation,
            "detail": fds.detail,
        },
        "family_consent": {
            "required": family.required,
            "contacts_to_verify": family.contacts_to_verify,
            "flow": family.flow,
            "detail": family.detail,
        },
        "audit": {
            "trace_id": audit_envelope["trace_id"],
            "ocp_version": audit_envelope["ocp_version"],
            "digest": audit_envelope["envelope_digest"],
        },
    }


# ──────────────────────────────────────────────────────────────────────────
# 정적 프론트엔드
# ──────────────────────────────────────────────────────────────────────────

@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
