"""
Z3 SMT 기반 형식 검증 — 금소법 §21 부당권유 금지 패턴.

학술 신규성 위치: 한국어 금융 도메인 LLM 출력의 형식 검증.
- 영어 자연어 추론(RuleBERT)·영어 법률 SMT(Stanford CodeX)는 존재
- 한국어 + 금융 + LLM 출력 검증은 미개척 (iter-0004-design.md §3 참조)

본 모듈은 LLM 출력(Seller view) 전체를 변수로 보고,
금소법 §21 위반 패턴이 substring으로 존재 가능한지 SMT solver로 형식 증명한다.

증명 결과는 OCP audit log에 `proof_artifact` 로 첨부된다.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from z3 import And, Bool, Not, Solver, sat, unsat


DATA_DIR = Path(__file__).parent / "data"


@dataclass
class VerificationResult:
    """Z3 검증 결과."""

    passed: bool
    principle_id: str
    principle_name: str
    matched_patterns: list[str]
    proof_summary: str
    smt_status: str  # "unsat" (위반 없음 증명) | "sat" (위반 가능성 존재)


def _load_fscma_kb() -> dict[str, Any]:
    with (DATA_DIR / "fscma_kb.json").open("r", encoding="utf-8") as fp:
        return json.load(fp)


def _verify_principle(
    text: str, principle: dict[str, Any]
) -> VerificationResult:
    """
    단일 금소법 원칙에 대한 SMT 검증.

    각 violation_signal s_i 에 대해 Bool 변수 b_i := (s_i in text) 를 사전 평가.
    Constraint: ∀i. ¬b_i  (어떤 위반 패턴도 출력에 포함되어서는 안 됨)
    Z3가 unsat 반환 시 → 위반 패턴 존재 (constraint 만족 불가능)
    Z3가 sat 반환 시 → 위반 패턴 없음 (constraint 만족)
    """
    signals: list[str] = principle["violation_signals"]
    solver = Solver()

    matched: list[str] = []
    bool_vars = []
    for idx, signal in enumerate(signals):
        var = Bool(f"contains_{principle['id']}_{idx}")
        bool_vars.append(var)
        present = signal in text
        if present:
            matched.append(signal)
        # 사실 사전 평가를 solver 에 주입
        solver.add(var == present)

    # 모든 패턴이 false 여야 통과
    no_violation = And([Not(v) for v in bool_vars])
    solver.add(no_violation)

    smt_result = solver.check()
    passed = smt_result == sat
    smt_status = "sat" if passed else "unsat"

    if passed:
        proof = (
            f"{principle['ref']} ({principle['name']}): "
            f"위반 패턴 {len(signals)}개 모두 부재 — Z3 sat 증명"
        )
    else:
        proof = (
            f"{principle['ref']} ({principle['name']}): "
            f"위반 패턴 {matched} 검출 — Z3 unsat (제약 위반)"
        )

    return VerificationResult(
        passed=passed,
        principle_id=principle["id"],
        principle_name=principle["name"],
        matched_patterns=matched,
        proof_summary=proof,
        smt_status=smt_status,
    )


def verify_seller_output(text: str) -> dict[str, Any]:
    """
    Seller LLM 출력 전체에 대한 금소법 6대 원칙 SMT 검증.
    부당권유(P5)·광고규제(P6)는 패턴 매칭으로 형식 검증 가능.
    설명의무(P3) 등 의미론적 항목은 LLM judge 로 별도 검증 (이 코드 외부).
    """
    kb = _load_fscma_kb()
    results: list[VerificationResult] = []
    for principle in kb["principles"]:
        # 패턴 검증이 의미 있는 원칙만 SMT 적용 (P5, P6)
        if principle["id"] in ("P5", "P6"):
            results.append(_verify_principle(text, principle))

    all_passed = all(r.passed for r in results)
    return {
        "kb_version": kb["version"],
        "verified_principles": [r.principle_id for r in results],
        "all_passed": all_passed,
        "results": [
            {
                "principle_id": r.principle_id,
                "principle_name": r.principle_name,
                "passed": r.passed,
                "smt_status": r.smt_status,
                "matched_patterns": r.matched_patterns,
                "proof": r.proof_summary,
            }
            for r in results
        ],
        "verifier": "Z3 SMT solver",
        "audit_note": (
            "본 검증은 부당권유·광고규제 패턴 검증에 한함. "
            "적합성·설명의무 등 의미론적 항목은 LLM-as-judge 와 RAG 인용 검증으로 보강."
        ),
    }


if __name__ == "__main__":
    # 자체 테스트
    bad = "이 ELS는 반드시 수익이 나며, 원금 보장이 됩니다. 100% 안전합니다."
    good = (
        "본 ELS는 기대 쿠폰이 연 최대 6.0% 수준이나, "
        "원금 손실 가능성이 있는 고위험 상품이므로 신중한 검토가 필요합니다."
    )
    print("=== BAD seller output ===")
    print(json.dumps(verify_seller_output(bad), ensure_ascii=False, indent=2))
    print("=== GOOD seller output ===")
    print(json.dumps(verify_seller_output(good), ensure_ascii=False, indent=2))
