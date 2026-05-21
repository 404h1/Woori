# 통합 시나리오 0 — 박영희 75세 + 손주 사칭 ELS

> 출처: `.omc/autoresearch/woori-advocate-grand-design/runs/run-001/iterations/iter-0004-design.md` §4
> 본 PoC: 단일 시연으로 응모 4분야(시니어·불완전판매·민원·보이스피싱) 동시 발동

## 등장 인물

- **박영희 (75세, 여)** — 우리은행 30년 거래 고객. 의료비 1,200만 원 최근 지출. 고위험 상품 거래 이력 5년간 0건. `senior_mode_eligible` 플래그.
- **자칭 손주 (010-0000-XXXX)** — 박영희에게 "할머니 ELS 좋대요, 3일 안에 해달래요" 압박. 24시간 전 24분간 통화.
- **실제 손주 박지민 (010-2222-XXXX)** — 박영희와 최근 6개월 통화 0건. 등록된 비상연락처.
- **자녀 박철수 (010-1111-XXXX)** — 등록된 비상연락처. 우리은행 안심앱 보유.
- **영업점 행원** — Seller view 보고 셀링 진행.

## 시연 timeline (≈12분)

| t (mm:ss) | 화면 / 음성 | 발표 멘트 |
|---|---|---|
| 00:00 | 영업점 입장, STT 동의 팝업 | "박영희 75세 고객 영업점 도착. STT 동의 후 자연 대화." |
| 00:30 | 행원 PC: Seller 셀링 포인트 자동 표시 | "행원은 셀링 가이드를 봅니다. 같은 LLM이 만든 강점 안내." |
| 01:00 | 박영희 태블릿: **시니어 모드 자동 활성화** (75세 ≥ 65) | "Senior 에이전트가 연령으로 자동 발동. 큰 글씨 + TTS." |
| 01:30 | STT: "손주가 좋대요, 3일 안에 해달래요" | "감정 분석이 '압박감' 패턴 검출 → 행원 PC 우상단 알람." |
| 02:00 | Advocate 5위험 좌우 분할 (또는 시니어는 한 화면씩) | "약관·고객 이력·통계 다층 검증. 5위험 항목 + 출처 표기." |
| 02:30 | Z3 SMT 검증 결과 표시: "금소법 §21·§22 통과" 또는 위반 패턴 표시 | "Seller 출력은 형식 논리로도 검증 — 수학적 증명." |
| 04:00 | 박영희가 1~5 모두 체크 + 가입 결정 | "Advocate는 차단이 아닌 조언. 본인 결정 존중." |
| 04:30 | ELS 가입 완료 → 송금 단계로 자동 진행 | |
| 05:00 | **FDS 발동**: 신규 계좌(3일 전) + 통화 이력 0회 + 평균 50배 거액 | "보이스피싱 시그널 4개 검출." |
| 05:30 | **Family Consent 발동**: 실제 손주에게 직접 통화 권유 | TTS: "박영희님, 손주 본인 번호로 전화 한 번만 부탁드려요." |
| 06:30 | 박영희가 진짜 손주 통화 → "ELS? 송금? 무슨 소리야?" | (배우 사전 녹음 또는 라이브) |
| 07:30 | 송금 차단 + ELS 가입 자동 취소(청약철회권 §47, 14일 내) | "금소법 §47로 14일 내 무조건 철회." |
| 08:00 | OCP audit trail JSON 표시 | "전 과정 5년 보관, 금감원·고객·법원 누구든 검증 가능." |
| 09:00 | A2A 메시지 로그 시각화 (Seller·Advocate·FDS·Family 협업) | "이질 LLM + Z3 형식 검증 + 외부 AI 호출 가능." |
| 10:00 | (선택) 박영희 외부 AI(Galaxy AI mock)가 Advocate 호출 | "고객측 AI 협상 — 세계 최초." |
| 11:00 | OCP 1.0 spec + Linux Foundation 로고 + 가상 KB·신한 채택 화면 | "한국 금융권 표준, 글로벌 reference." |
| 12:00 | "DLF 197억의 회사가 한국 금융권 소비자보호 표준의 출처가 됩니다" | 슬로건 + Q&A |

## 4분야 동시 발동 매트릭스

| 응모분야 | 발동 에이전트 | 결정 근거 |
|---|---|---|
| 1. 취약계층 보호 | Senior + Family Consent | `senior_mode_eligible` 플래그, 연령 75 |
| 2. 불완전판매 예방 | Advocate + Z3 + Moderator | 적합성 위반 (이력 0건 vs 적극투자형 자가설문 불일치), 약관 출처 검증 |
| 3. 민원 사전 예방 | (감정 분석 — 본 PoC 외) | "압박감" 패턴 → 행원 알람 → 사전 면담 |
| 4. 보이스피싱 예방 | FDS + Family Consent | 평소 50배 거액 + 신규 계좌 + 통화 이력 0회 + 의심 발신 통화 |

## PoC 에서 실제 작동하는 부분 vs 시연 mock

| 컴포넌트 | PoC 상태 |
|---|---|
| Seller LLM | ✅ 실작동 — claude-agent-sdk |
| Advocate LLM | ✅ 실작동 — claude-agent-sdk |
| Moderator (인용 검증) | ✅ 실작동 — Python 룰 |
| Z3 SMT (금소법 §21·§22) | ✅ 실작동 — z3-solver |
| Senior 자동 활성 | ✅ 실작동 — 연령·플래그 |
| FDS (송금 단계) | ✅ 실작동 — 룰 기반 |
| Family Consent | ✅ 실작동 — 룰 기반 (실제 푸시는 mock) |
| OCP audit log | ✅ 실작동 — JSONL append |
| Agent Card (.well-known) | ✅ 실작동 |
| 감정 분석 (민원 예방) | ⚠️ Phase 2 — 본 PoC 미포함 |
| 고객측 AI 협상 | ⚠️ Phase 3 — Agent Card 노출로만 시연 |
| OCP 컨소시엄 인증 | ⚠️ Phase 4 — PPT narrative |

## 실행 명령

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# 브라우저: http://localhost:8000
# 박영희 ELS 시연 버튼 → 체크 → 가입 → 송금 → FDS+Family
```

## Q&A 시 활용 포인트

- "왜 5위험만?" → 약관 청크에서 RAG 검색된 6개 청크 중 고객 프로필 매핑 후 5개 도출. iter-0001 §3 참조.
- "Seller·Advocate 같은 LLM인데 진짜 대립?" → 본 PoC는 동일 모델(Claude default)이지만 system_prompt·context 완전 격리. 풀 grand design은 이질 모델 (iter-0002 §1).
- "Z3가 한국어 자연어를 검증?" → 추출된 토큰 패턴만 SMT. 의미 검증은 LLM-as-judge로 별도. iter-0004 §3 참조.
- "Phase 4·5 글로벌은?" → grand design iter-0004 §6 참조 (OCP 표준 + 5개국 진출). 본 PoC는 Phase 0~1.
