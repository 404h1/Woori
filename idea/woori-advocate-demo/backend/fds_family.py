"""
FDS (Fraud Detection System) + Family Consent — 통합 시나리오 0 보조 에이전트.

본 PoC 는 룰 기반. iter-0003 design 의 통합 시나리오 0 (박영희 75세 + 손주 사칭 ELS) 가
끝난 후, 가입 자금을 손주 계좌로 송금하려는 단계에서 발동된다.

실서비스에서는 GNN + transformer FDS 모델, 통신사 STT 연동, 가족 동의 앱 푸시 연동.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


@dataclass
class FDSResult:
    risk_score: float  # 0.0 ~ 1.0
    triggered_signals: list[str]
    recommendation: str  # "PROCEED" | "DELAY" | "BLOCK"
    detail: dict[str, Any]


@dataclass
class FamilyConsentResult:
    required: bool
    contacts_to_verify: list[dict[str, str]]
    flow: list[str]  # 절차 단계 텍스트
    detail: dict[str, Any]


def evaluate_fds(customer: dict[str, Any], transfer: dict[str, Any]) -> FDSResult:
    """
    통합 시나리오 0 의 송금 단계 FDS.
    transfer = {
        amount_krw: int,
        recipient_account_age_days: int,
        recipient_claimed_relation: "손주" | ...,
        recipient_actual_call_history_6m_count: int,
    }
    """
    signals: list[str] = []
    score = 0.0

    amount = transfer.get("amount_krw", 0)
    avg_transfer = customer["profile"].get("monthly_avg_transfer_krw", 1)
    if amount >= avg_transfer * 50:
        signals.append(
            f"비정상 거액: 평소 평균 이체액의 {amount / max(avg_transfer, 1):.0f}배"
        )
        score += 0.3

    if transfer.get("recipient_account_age_days", 999) <= 7:
        signals.append("수취 계좌 최근 개설 (≤7일)")
        score += 0.25

    if transfer.get("recipient_actual_call_history_6m_count", 999) == 0:
        signals.append(
            f"자칭 '{transfer.get('recipient_claimed_relation', '관계자')}' 와 최근 6개월 통화 이력 0회"
        )
        score += 0.25

    # 최근 24시간 의심 통화
    incoming = customer.get("recent_activity", {}).get("incoming_calls_last_24h", [])
    if any(call.get("duration_sec", 0) > 600 for call in incoming):
        signals.append("최근 24시간 내 장시간(>10분) 의심 발신 통화 존재")
        score += 0.2

    score = min(score, 1.0)
    if score >= 0.7:
        recommendation = "BLOCK"
    elif score >= 0.4:
        recommendation = "DELAY"
    else:
        recommendation = "PROCEED"

    return FDSResult(
        risk_score=round(score, 3),
        triggered_signals=signals,
        recommendation=recommendation,
        detail={
            "model": "rule-based-v1 (mock)",
            "note": "실서비스: GNN+transformer FDS + 통신사 STT 융합",
            "thresholds": {"BLOCK": 0.7, "DELAY": 0.4},
        },
    )


def request_family_consent(
    customer: dict[str, Any], fds: FDSResult
) -> FamilyConsentResult:
    """
    FDS 가 DELAY/BLOCK 으로 판정한 거래에 대해 가족 동의 절차 발동.
    """
    if fds.recommendation == "PROCEED":
        return FamilyConsentResult(
            required=False, contacts_to_verify=[], flow=[], detail={"reason": "FDS PROCEED"}
        )

    contacts = customer.get("recent_activity", {}).get("registered_emergency_contacts", [])
    deadline = datetime.now() + timedelta(minutes=30)
    flow = [
        "1. 박영희님 본인 휴대전화로 등록된 손주(박지민) 번호 010-2222-XXXX 직접 통화 확인.",
        "2. 동시에 자녀(박철수)에게 우리은행 안심앱 푸시 → '이체 동의 요청' 알림 발송.",
        f"3. {deadline.strftime('%H:%M')} 까지 1·2 모두 미응답 시 우리은행 안심센터 자동 연결.",
        "4. 동의 완료까지 송금 보류, 시니어 모드 TTS 로 절차 안내.",
    ]
    return FamilyConsentResult(
        required=True,
        contacts_to_verify=contacts,
        flow=flow,
        detail={
            "deadline_iso": deadline.isoformat(),
            "channels": ["voice_call", "wb_safe_push", "wb_safety_center"],
        },
    )
