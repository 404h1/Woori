"""
Seller / Advocate / Moderator — providers.py 위에서 동작.

- Seller   → providers.AnthropicProvider  (API key → CLI OAuth → mock)
- Advocate → providers.OpenAIProvider  (API key → CLI OAuth → mock)

iter-0002-design.md §1 의 이질 LLM ensemble 을 ZeroClaw multi-auth 패턴으로
구현. 환경에 따라 자동 fallback.

WOORI_DEMO_MODE=cache 환경변수 설정 시 backend/data/demo_cache/ 의 사전 캐시
응답을 즉시 반환 (시연 안정성·인터넷 장애·LLM 지연 대비).
"""
from __future__ import annotations

import asyncio
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from providers import LLMCallResult, get_provider

DATA_DIR = Path(__file__).parent / "data"
DEMO_CACHE_DIR = DATA_DIR / "demo_cache"
DEMO_MODE = os.environ.get("WOORI_DEMO_MODE", "").lower() == "cache"
SELLER_PROVIDER = "anthropic"


# ──────────────────────────────────────────────────────────────────────────
# System prompts (Constitutional 스타일)
# ──────────────────────────────────────────────────────────────────────────

SELLER_SYSTEM_PROMPT = """\
당신은 우리은행 행원의 판매 보조 AI 'Seller' 입니다.

[헌법]
1. 단정적·확약 표현 금지: '반드시', '확실', '100%', '보장', '손실 없', '절대 안전', '원금 보장', '수익 확정', '무조건' 사용 절대 금지.
2. 미래 수익률은 항상 '예상' 또는 '최대' 표현 사용.
3. 고객 개인 프로필을 입력받지 않으므로 개인 정보 추론 금지.
4. 출력은 글머리 기호 3~4개로만, 각 1~2문장.
5. 톤: 정중·전문·간결.

[제공된 자료]
{product_summary}

[지침]
위 자료 범위 내에서 상품의 강점 3~4개를 글머리 기호(▸ 사용)로 작성하시오.
한국어로만 답하시오. 추가 설명·서두 없이 글머리 항목만 출력하시오.
"""


ADVOCATE_SYSTEM_PROMPT = """\
당신은 고객 편에서 위험을 짚는 AI 'Advocate' 입니다.

[헌법]
1. 제공된 [약관 청크] 와 [고객 프로필] 범위 밖의 사실 인용 절대 금지.
2. 각 위험 항목 끝에 [출처: 청크ID] 표기 필수.
3. 평어·구체 수치 사용, 고객 본인 데이터 매핑.
4. 단정 X — '~할 수 있습니다', '~우려가 있습니다' 사용.
5. 최대 5개 항목.

[약관 청크]
{terms_chunks}

[고객 프로필]
{customer_profile}

[출력 형식 — JSON only, 그 외 텍스트 절대 금지]
{{
  "items": [
    {{"no": 1, "title": "...", "explanation": "...", "source": "T-NNN"}}
  ]
}}

한국어 JSON 만 출력. 코드블록 마커 (```) 사용 금지. 설명문 금지.
"""


# ──────────────────────────────────────────────────────────────────────────
# Mock fallback responses
# ──────────────────────────────────────────────────────────────────────────

MOCK_SELLER_RESPONSE = """\
▸ 시중 예적금 대비 약 3배 수준인 연 최대 6.0% 세전 쿠폰을 기대할 수 있는 ELS 상품입니다.
▸ 매 6개월 평가일에 조기상환 조건이 충족되면 만기 이전 상환이 가능합니다.
▸ 본 상품은 적극투자형 이상 고객을 위한 원금비보장형 파생결합증권입니다.
▸ 만기 평가일 기초자산이 일정 기준 이상이면 약정 쿠폰을 수령할 수 있습니다.\
"""

MOCK_ADVOCATE_RESPONSE = {
    "items": [
        {
            "no": 1,
            "title": "3년간 자금 묶임 (유동성 제약)",
            "explanation": (
                "본 상품은 만기 36개월의 폐쇄형으로, 중도해지 시 환매수수료 및 평가손실이 발생할 수 있습니다. "
                "박영희님의 최근 의료비 1,200만원 지출 이력을 고려할 때, 예기치 못한 병원비 비상금 마련에 차질이 생길 수 있습니다."
            ),
            "source": "T-002",
        },
        {
            "no": 2,
            "title": "실질 고위험 상품 거래 경험 부재",
            "explanation": (
                "약관 §2.3 적합성 원칙은 '고위험 상품 거래 경험이 있는 고객' 을 적합 대상으로 정합니다. "
                "박영희님의 우리은행 거래 기록상 최근 5년간 원금비보장형 고위험 상품 가입 이력이 확인되지 않습니다."
            ),
            "source": "T-004",
        },
        {
            "no": 3,
            "title": "원금 최대 100% 손실 가능",
            "explanation": (
                "만기 평가일 홍콩H지수가 가입일 대비 -50% 이상 하락할 경우, 원금의 최대 100%까지 손실이 발생할 수 있습니다."
            ),
            "source": "T-001",
        },
        {
            "no": 4,
            "title": "유사 상품 실측 손실률",
            "explanation": (
                "직전 24개월 유사 ELS 만기 도래분 중 7.2%에서 원금 손실이 발생했으며, 평균 손실률은 -38.4%로 기록되어 있습니다."
            ),
            "source": "T-006",
        },
        {
            "no": 5,
            "title": "기초자산의 단기 변동성",
            "explanation": (
                "홍콩H지수는 중국 본토 정책·홍콩 정치적 환경·환율 변동 등 다양한 요인으로 단기간 큰 변동이 발생할 수 있어, "
                "75세 시니어 고객의 안정적 자금 운용 목적에 부합하지 않을 우려가 있습니다."
            ),
            "source": "T-005",
        },
    ]
}


# ──────────────────────────────────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────────────────────────────────

def load_customer(customer_id: str) -> dict[str, Any]:
    with (DATA_DIR / f"{customer_id}.json").open("r", encoding="utf-8") as fp:
        return json.load(fp)


def load_product(product_id: str) -> dict[str, Any]:
    with (DATA_DIR / "els_hongkong_h.json").open("r", encoding="utf-8") as fp:
        return json.load(fp)


def load_terms_chunks(product_id: str) -> list[dict[str, str]]:
    with (DATA_DIR / "els_terms_chunks.json").open("r", encoding="utf-8") as fp:
        return json.load(fp)["chunks"]


# ──────────────────────────────────────────────────────────────────────────
# Agent outputs
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class SellerOutput:
    text: str
    backend: str
    model_hint: str


@dataclass
class AdvocateOutput:
    items: list[dict[str, str]]
    backend: str
    model_hint: str
    raw_text: str = ""


# ──────────────────────────────────────────────────────────────────────────
# Seller (Claude/Anthropic provider)
# ──────────────────────────────────────────────────────────────────────────

async def run_seller(product: dict[str, Any]) -> SellerOutput:
    # 데모 모드: 사전 캐시 반환
    if DEMO_MODE:
        cache_file = DEMO_CACHE_DIR / "scenario_0_seller.txt"
        if cache_file.exists():
            return SellerOutput(
                text=cache_file.read_text(encoding="utf-8").strip(),
                backend="demo-cache", model_hint="cache-seller",
            )

    product_summary = json.dumps(
        {
            "name": product["name"],
            "category": product["category"],
            "tenor_months": product["tenor_months"],
            "max_coupon_pct_annual": product["max_coupon_pct_annual"],
            "knock_in_pct": product["knock_in_pct"],
            "early_redemption_schedule": product["early_redemption_schedule"],
        },
        ensure_ascii=False,
        indent=2,
    )
    sys_prompt = SELLER_SYSTEM_PROMPT.format(product_summary=product_summary)
    user_prompt = (
        "위 상품의 강점을 행원이 박영희(75세) 고객에게 설명할 때 "
        "사용할 셀링 포인트 3~4개를 작성하시오. "
        "고객 프로필은 절대 가정·추론하지 마시오."
    )

    result = await get_provider(SELLER_PROVIDER).call(sys_prompt, user_prompt)
    if result.backend == "mock" or not result.text:
        return SellerOutput(text=MOCK_SELLER_RESPONSE, backend="mock",
                            model_hint=result.model_hint or f"mock-{SELLER_PROVIDER}")
    return SellerOutput(text=result.text, backend=result.backend, model_hint=result.model_hint)


# ──────────────────────────────────────────────────────────────────────────
# Advocate (OpenAI provider)
# ──────────────────────────────────────────────────────────────────────────

def _safe_parse_advocate_json(text: str) -> dict[str, Any] | None:
    cleaned = re.sub(r"```(?:json)?", "", text).strip("` \n\t")
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    candidate = cleaned[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


async def run_advocate(
    customer: dict[str, Any],
    product: dict[str, Any],
    terms_chunks: list[dict[str, str]],
) -> AdvocateOutput:
    # 데모 모드: 사전 캐시 반환
    if DEMO_MODE:
        cache_file = DEMO_CACHE_DIR / "scenario_0_advocate.json"
        if cache_file.exists():
            with cache_file.open("r", encoding="utf-8") as fp:
                cached = json.load(fp)
            return AdvocateOutput(
                items=cached.get("items", []),
                backend="demo-cache", model_hint="cache-advocate",
            )

    chunks_text = "\n".join(
        f"[{c['id']}] {c['section']}: {c['text']}" for c in terms_chunks
    )
    profile_min = {
        "age": customer["age"],
        "investment_propensity_self_reported": customer["profile"][
            "investment_propensity_self_reported"
        ],
        "high_risk_product_history_5y": customer["profile"]["high_risk_product_history_5y"],
        "recent_large_expenses_3m": customer["profile"]["recent_large_expenses_3m"],
        "accessibility_flags": customer["profile"]["accessibility_flags"],
    }
    profile_text = json.dumps(profile_min, ensure_ascii=False, indent=2)
    sys_prompt = ADVOCATE_SYSTEM_PROMPT.format(
        terms_chunks=chunks_text, customer_profile=profile_text
    )
    user_prompt = (
        f"고객 {customer['name']} ({customer['age']}세) 이 본 ELS 상품에 "
        "맞지 않을 수 있는 5가지 이유를 JSON 으로 출력하시오. "
        "각 항목은 약관 청크에 출처가 있어야 합니다. JSON 외 어떤 텍스트도 출력 금지."
    )

    result = await get_provider("openai").call(sys_prompt, user_prompt)
    if result.backend == "mock" or not result.text:
        return AdvocateOutput(items=MOCK_ADVOCATE_RESPONSE["items"], backend="mock",
                              model_hint=result.model_hint or "mock-openai")
    parsed = _safe_parse_advocate_json(result.text)
    if parsed is None or "items" not in parsed:
        return AdvocateOutput(
            items=MOCK_ADVOCATE_RESPONSE["items"],
            backend="mock-fallback",
            model_hint=result.model_hint,
            raw_text=result.text,
        )
    return AdvocateOutput(
        items=parsed["items"],
        backend=result.backend,
        model_hint=result.model_hint,
        raw_text=result.text,
    )


# ──────────────────────────────────────────────────────────────────────────
# 병렬 fan-out (Round 1 — 독립 호출)
# ──────────────────────────────────────────────────────────────────────────

async def run_seller_and_advocate(
    customer: dict[str, Any],
    product: dict[str, Any],
    terms_chunks: list[dict[str, str]],
) -> tuple[SellerOutput, AdvocateOutput]:
    return await asyncio.gather(  # type: ignore[return-value]
        run_seller(product), run_advocate(customer, product, terms_chunks)
    )


# ──────────────────────────────────────────────────────────────────────────
# Multi-Agent Debate (MAD) — cross-context embedding
#
# 임베딩의 본질: Round N 에서 상대 LLM 의 출력 텍스트를 내 system prompt context
# 에 embedding 시킨다. 단순 병렬과 달리 진짜 "토론" 이 발생.
#
# MIT MAD (ICML 2024) 의 +80.9% accuracy 향상은 이 cross-context embedding 에서
# 발생. 단순 prompt 격리 만으로는 토론 효과 없음.
# ──────────────────────────────────────────────────────────────────────────

SELLER_REBUTTAL_PROMPT = """\
당신은 우리은행의 Seller AI 입니다. 이미 1차 셀링 포인트를 제시했고,
같은 사건에 대해 'Advocate' AI 가 고객 측 위험을 제기했습니다.

[당신의 1차 셀링 포인트]
{seller_prev}

[Advocate 의 1차 위험 제기]
{advocate_prev}

[임무]
1. Advocate 의 위험 중 합리적인 것은 인정한다.
2. 단, 본질적 강점은 유지하되 단정·확약 표현 금지 (헌법 동일).
3. 균형을 잡되 셀링 포지션은 포기하지 않는다.
4. 글머리 기호 3~4개로 재작성 — 각 1~2문장.
5. 한국어만, 서두·설명 없이 글머리 항목만 출력.

[헌법]
- 금지어: '반드시', '확실', '100%', '보장', '손실 없', '절대 안전', '원금 보장', '수익 확정', '무조건'
"""


ADVOCATE_REBUTTAL_PROMPT = """\
당신은 고객 측 Advocate AI 입니다. 이미 1차로 5위험을 제시했고,
같은 사건에 대해 'Seller' AI 가 셀링 포인트를 제시했습니다.

[당신의 1차 위험 제기]
{advocate_prev}

[Seller 의 셀링 포인트]
{seller_prev}

[약관 청크]
{terms_chunks}

[고객 프로필]
{customer_profile}

[임무]
1. Seller 의 주장 중 위험으로 재구성 가능한 것이 있는지 검토.
2. 1차에서 놓친 위험이 Seller 발언으로 인해 드러난다면 추가.
3. 약관 청크 범위 밖 사실 인용 절대 금지. 출처 청크 ID 필수.
4. 최대 5개 항목으로 재정리 (1차 항목 + 신규/강화 모두 포함, 우선순위 재배열).

[출력 형식 — JSON only]
{{
  "items": [
    {{"no": 1, "title": "...", "explanation": "...", "source": "T-NNN"}}
  ]
}}

한국어 JSON 만 출력. 코드블록 금지.
"""


CONSENSUS_PROMPT = """\
당신은 중립 Moderator 입니다. Seller 와 Advocate 가 2 라운드 토론을 마쳤습니다.

[Seller 최종 입장]
{seller_final}

[Advocate 최종 입장]
{advocate_final}

[임무]
두 입장이 어디서 합의했고 어디서 명시적 불일치가 남았는지 1~2문장으로 요약.
판단 X — 사실 정리만.

[출력 형식 — JSON only]
{{
  "agreed": ["합의된 사실 1~3개"],
  "disagreed": ["불일치 항목 0~2개"],
  "verdict": "balanced | leans_advocate | leans_seller"
}}
"""


@dataclass
class DebateRound:
    round_num: int
    seller_text: str
    seller_backend: str
    advocate_items: list[dict[str, str]]
    advocate_backend: str


@dataclass
class DebateConsensus:
    agreed: list[str]
    disagreed: list[str]
    verdict: str
    raw_text: str = ""


async def _seller_rebuttal(
    product: dict[str, Any],
    prev_seller: str,
    prev_advocate_items: list[dict[str, str]],
) -> SellerOutput:
    """Round 2 Seller — Advocate 의 위험 제기를 context 에 embedding 후 재작성."""
    if DEMO_MODE:
        cache = DEMO_CACHE_DIR / "scenario_0_seller_r2.txt"
        if cache.exists():
            return SellerOutput(
                text=cache.read_text(encoding="utf-8").strip(),
                backend="demo-cache", model_hint="cache-seller-r2",
            )

    adv_summary = "\n".join(
        f"  - {i.get('no')}. {i.get('title')} [{i.get('source')}]"
        for i in prev_advocate_items
    )
    sys_prompt = SELLER_REBUTTAL_PROMPT.format(
        seller_prev=prev_seller, advocate_prev=adv_summary,
    )
    user_prompt = (
        "위 토론 컨텍스트를 반영하여 셀링 포인트를 균형 잡힌 형태로 재작성하시오. "
        "Advocate 가 제기한 위험을 부정하지 말고, 인정하면서 가치를 설명하시오."
    )
    result = await get_provider(SELLER_PROVIDER).call(sys_prompt, user_prompt)
    if result.backend == "mock" or not result.text:
        return SellerOutput(text=MOCK_SELLER_RESPONSE, backend="mock",
                            model_hint=result.model_hint or "mock-r2")
    return SellerOutput(text=result.text, backend=result.backend,
                        model_hint=result.model_hint + "-r2")


async def _advocate_rebuttal(
    customer: dict[str, Any],
    terms_chunks: list[dict[str, str]],
    prev_advocate: list[dict[str, str]],
    prev_seller: str,
) -> AdvocateOutput:
    """Round 2 Advocate — Seller 의 반박을 보고 위험을 재정리."""
    if DEMO_MODE:
        cache = DEMO_CACHE_DIR / "scenario_0_advocate_r2.json"
        if cache.exists():
            with cache.open("r", encoding="utf-8") as fp:
                cached = json.load(fp)
            return AdvocateOutput(
                items=cached.get("items", []),
                backend="demo-cache", model_hint="cache-advocate-r2",
            )

    chunks_text = "\n".join(
        f"[{c['id']}] {c['section']}: {c['text']}" for c in terms_chunks
    )
    profile_min = {
        "age": customer["age"],
        "investment_propensity_self_reported": customer["profile"][
            "investment_propensity_self_reported"],
        "high_risk_product_history_5y": customer["profile"]["high_risk_product_history_5y"],
        "recent_large_expenses_3m": customer["profile"]["recent_large_expenses_3m"],
        "accessibility_flags": customer["profile"]["accessibility_flags"],
    }
    profile_text = json.dumps(profile_min, ensure_ascii=False, indent=2)
    adv_summary = json.dumps(
        {"items": [{"no": i.get("no"), "title": i.get("title"),
                    "source": i.get("source")} for i in prev_advocate]},
        ensure_ascii=False, indent=2,
    )

    sys_prompt = ADVOCATE_REBUTTAL_PROMPT.format(
        advocate_prev=adv_summary, seller_prev=prev_seller,
        terms_chunks=chunks_text, customer_profile=profile_text,
    )
    user_prompt = (
        "Seller 의 반박/주장을 검토하고 위험 항목을 재정리하시오. "
        "약관 청크 범위 내에서만, 출처 ID 필수. JSON 만 출력."
    )
    result = await get_provider("openai").call(sys_prompt, user_prompt)
    if result.backend == "mock" or not result.text:
        return AdvocateOutput(items=MOCK_ADVOCATE_RESPONSE["items"],
                              backend="mock", model_hint=result.model_hint or "mock-r2")
    parsed = _safe_parse_advocate_json(result.text)
    if parsed is None or "items" not in parsed:
        return AdvocateOutput(
            items=MOCK_ADVOCATE_RESPONSE["items"], backend="mock-fallback",
            model_hint=result.model_hint + "-r2", raw_text=result.text,
        )
    return AdvocateOutput(items=parsed["items"], backend=result.backend,
                          model_hint=result.model_hint + "-r2", raw_text=result.text)


async def _consensus(seller_final: str, advocate_items: list[dict[str, str]]) -> DebateConsensus:
    """Moderator 합의 추출 — OpenAI provider 로 안정적으로 처리."""
    if DEMO_MODE:
        cache = DEMO_CACHE_DIR / "scenario_0_consensus.json"
        if cache.exists():
            with cache.open("r", encoding="utf-8") as fp:
                cached = json.load(fp)
            return DebateConsensus(
                agreed=cached.get("agreed", []),
                disagreed=cached.get("disagreed", []),
                verdict=cached.get("verdict", "balanced"),
            )

    adv_final = "\n".join(
        f"  - {i.get('no')}. {i.get('title')}: {i.get('explanation','')[:120]}"
        for i in advocate_items
    )
    sys_prompt = CONSENSUS_PROMPT.format(
        seller_final=seller_final, advocate_final=adv_final,
    )
    user_prompt = "두 입장의 합의/불일치를 JSON 으로 정리하시오."
    # Consensus 는 openai 로 (codex CLI 안정성)
    result = await get_provider("openai").call(sys_prompt, user_prompt)
    if result.backend == "mock" or not result.text:
        return DebateConsensus(
            agreed=["원금 손실 가능성", "75세 시니어 안정성 우선"],
            disagreed=["가입 진행 vs 보류"],
            verdict="leans_advocate",
        )
    parsed = _safe_parse_advocate_json(result.text)
    if parsed is None:
        return DebateConsensus(
            agreed=[], disagreed=[], verdict="balanced",
            raw_text=result.text,
        )
    return DebateConsensus(
        agreed=parsed.get("agreed", []),
        disagreed=parsed.get("disagreed", []),
        verdict=parsed.get("verdict", "balanced"),
        raw_text=result.text,
    )


async def run_mad_debate(
    customer: dict[str, Any],
    product: dict[str, Any],
    terms_chunks: list[dict[str, str]],
    rounds: int = 2,
) -> tuple[list[DebateRound], DebateConsensus]:
    """
    Multi-Agent Debate — N 라운드 토론 + consensus.

    Round 1: 독립 호출 (parallel, 서로 못 봄)
    Round 2~N: 각자 상대의 직전 출력을 context 에 embedding 후 재작성
    최종: Moderator 가 합의/불일치 추출
    """
    history: list[DebateRound] = []

    # Round 1 — 독립
    s1, a1 = await run_seller_and_advocate(customer, product, terms_chunks)
    history.append(DebateRound(
        round_num=1,
        seller_text=s1.text, seller_backend=f"{s1.backend} · {s1.model_hint}",
        advocate_items=a1.items, advocate_backend=f"{a1.backend} · {a1.model_hint}",
    ))

    cur_seller_text = s1.text
    cur_advocate_items = a1.items

    # Round 2~N — cross-context embedding
    for r in range(2, rounds + 1):
        # 두 호출을 병렬 실행 (각자 R-1 상대 출력 사용)
        s_r, a_r = await asyncio.gather(
            _seller_rebuttal(product, cur_seller_text, cur_advocate_items),
            _advocate_rebuttal(customer, terms_chunks, cur_advocate_items, cur_seller_text),
        )
        history.append(DebateRound(
            round_num=r,
            seller_text=s_r.text, seller_backend=f"{s_r.backend} · {s_r.model_hint}",
            advocate_items=a_r.items, advocate_backend=f"{a_r.backend} · {a_r.model_hint}",
        ))
        cur_seller_text = s_r.text
        cur_advocate_items = a_r.items

    # Consensus
    consensus = await _consensus(cur_seller_text, cur_advocate_items)
    return history, consensus


# ──────────────────────────────────────────────────────────────────────────
# Moderator — 인용 검증 (룰 기반)
# ──────────────────────────────────────────────────────────────────────────

def moderate_advocate_items(
    items: list[dict[str, str]], terms_chunks: list[dict[str, str]]
) -> dict[str, Any]:
    chunk_by_id = {c["id"]: c for c in terms_chunks}
    findings = []
    for item in items:
        src_id = item.get("source", "")
        chunk = chunk_by_id.get(src_id)
        if chunk is None:
            findings.append({
                "no": item.get("no"),
                "source_id": src_id,
                "verified": False,
                "reason": "출처 청크 ID 없음 — 환각 가능성",
            })
            continue
        nums = re.findall(r"\d+", item.get("explanation", ""))
        nums_in_chunk = [n for n in nums if n in chunk["text"]]
        findings.append({
            "no": item.get("no"),
            "source_id": src_id,
            "verified": True,
            "matched_numbers": nums_in_chunk,
            "chunk_section": chunk["section"],
        })
    return {
        "checker": "moderator-rule-v1",
        "items_total": len(items),
        "items_verified": sum(1 for f in findings if f["verified"]),
        "findings": findings,
    }
