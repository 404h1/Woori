"""
OCP (Open Consumer Protection) audit log.

iter-0003-design.md §1 의 OCP 표준 의 PoC 구현.
모든 Advocate 개입을 표준 JSON 메시지로 직렬화 → 금감원·EU AI Act 감사 trail.

실서비스: append-only 분산 로그 (CockroachDB / immudb 등) + 금감원 audit endpoint POST.
PoC: 메모리 + 파일 append.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any


AUDIT_FILE = Path(__file__).parent / "data" / "ocp_audit.log.jsonl"
_LOCK = Lock()

OCP_VERSION = "1.0-poc"
AGENT_CARD = {
    "ocp_version": OCP_VERSION,
    "agent": {
        "name": "Woori Advocate",
        "issuer": "우리은행 금융소비자보호그룹 (PoC)",
        "endpoint": "/api/review",
        "skills": [
            {
                "id": "ocp.advocate.review",
                "input_schema": "ocp.types.ProductReviewRequest",
                "output_schema": "ocp.types.AdvocateOpinion",
            },
            {
                "id": "ocp.compliance.fscma_proof",
                "output_schema": "ocp.types.FormalProof",
                "verifier": "Z3",
            },
            {
                "id": "ocp.fraud.transfer_check",
                "input_schema": "ocp.types.TransferRequest",
                "output_schema": "ocp.types.FDSVerdict",
            },
        ],
    },
    "regulator_endpoints": {
        "fss": "https://api.fss.or.kr/ocp/v1/audit (mock)",
        "fsc": "https://api.fsc.go.kr/ocp/v1/notify (mock)",
    },
    "audit_retention": "5y",
    "constitutional_kb": {
        "version": "fscma-2026.01",
        "path": "backend/data/fscma_kb.json",
    },
}


def _digest(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()[:32]


def append_audit(
    customer_id: str,
    product_id: str,
    seller_meta: dict[str, Any],
    advocate_meta: dict[str, Any],
    z3_proof: dict[str, Any],
    moderator: dict[str, Any],
    fds: dict[str, Any] | None = None,
    family_consent: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Append-only audit 기록. 표준 envelope 반환."""
    envelope = {
        "ocp_version": OCP_VERSION,
        "trace_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "customer_id_hash": "sha256:" + hashlib.sha256(customer_id.encode()).hexdigest()[:16],
        "product_id": product_id,
        "agents": {
            "seller": seller_meta,
            "advocate": advocate_meta,
        },
        "formal_proof": z3_proof,
        "moderator": moderator,
        "fds": fds,
        "family_consent": family_consent,
    }
    envelope["envelope_digest"] = _digest(envelope)

    with _LOCK:
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT_FILE.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(envelope, ensure_ascii=False) + "\n")

    return envelope


def get_agent_card() -> dict[str, Any]:
    return AGENT_CARD


def read_recent_audits(limit: int = 20) -> list[dict[str, Any]]:
    if not AUDIT_FILE.exists():
        return []
    with AUDIT_FILE.open("r", encoding="utf-8") as fp:
        lines = fp.readlines()
    return [json.loads(line) for line in lines[-limit:]]
