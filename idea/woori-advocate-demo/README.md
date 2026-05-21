# Woori Advocate — Grand Design 압축 PoC

> 같은 LLM을 두 페르소나(Seller·Advocate)로 격리, 고위험 상품 가입 직전 좌우 분할로 동시 출력.
> [iter-0004-design.md](../.omc/autoresearch/woori-advocate-grand-design/runs/run-001/iterations/iter-0004-design.md) 의 grand design 을 PoC 수준으로 압축한 구현체.

## 무엇이 작동하나

- **이질 LLM MAD (Multi-Agent Debate)** — iter-0002 §1 의 literal 매핑 + cross-context embedding
  - **Seller   → Claude** (`claude` subprocess, Claude OAuth, `~/.claude/` 세션 / `ANTHROPIC_API_KEY` REST)
  - **Advocate → OpenAI GPT** (`codex exec` subprocess, ChatGPT OAuth / `OPENAI_API_KEY` REST)
  - 두 LLM 이 서로 다른 학습 데이터·정렬 철학 → Q5 "같은 LLM 진짜 대립?" 답 강화
  - **`POST /api/review_mad?rounds=2`** — 라운드 N에서 상대 출력이 내 system prompt 에 embedding → 진짜 토론 발생
  - MIT MAD ICML 2024 의 +80.9% 정확도 향상 literal 적용
- **Z3 SMT 형식 검증** — Seller 출력에 금소법 §21·§22 부당권유·광고 패턴 형식 증명
- **Moderator 인용 검증** — Advocate 항목의 출처 청크 ID + 핵심 수치 substring 매칭
- **시니어 모드 자동 활성화** — `senior_mode_eligible` 플래그 + 연령 ≥65, TTS (Web Speech API)
- **FDS + Family Consent** — 송금 단계, 룰 기반 보이스피싱 신호 검출
- **OCP audit log** — 표준 envelope JSONL append, Agent Card `.well-known/agent.json` 노출
- **통합 시나리오 0** — 박영희 75세 + 손주 사칭 ELS (응모 4분야 동시 발동)

PoC 외 (Phase 2~5)는 [scenarios/scenario_0_integrated.md](scenarios/scenario_0_integrated.md) "PoC vs mock" 표 참조.

## 빠른 실행 (Windows / macOS / Linux)

### 1) LLM Provider 인증 (3단 폴백 — OpenClaw/ZeroClaw 패턴 차용)

**우선순위:** API key (env) → CLI OAuth → Mock fallback

#### 선택 A — API key (가장 안정, 권장)

```bash
# Claude (Seller)
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI GPT (Advocate)
export OPENAI_API_KEY="sk-..."
# https://platform.openai.com/api-keys
```

#### 선택 B — CLI OAuth (무료 티어 활용)

```bash
# Claude
npm i -g @anthropic-ai/claude-code
claude                                          # 브라우저 OAuth → ~/.claude/ 세션
claude -p "Say OK." --output-format text        # backend 실행 전 인증 확인

# OpenClaw식 헤드리스/장기 실행 대안
claude setup-token
export CLAUDE_CODE_OAUTH_TOKEN="..."            # Windows PowerShell: $env:CLAUDE_CODE_OAUTH_TOKEN="..."

# Codex (GPT)
npm i -g @openai/codex && codex login    # 브라우저 OAuth → ~/.codex/ 캐시
```

OpenClaw 문서 기준으로도 Anthropic은 API key가 가장 예측 가능한 경로이고, 구독/OAuth 재사용은 토큰을 직접 API처럼 호출하기보다 공식 `claude -p` CLI를 재사용하는 방식이 선호된다. 이 PoC도 Seller를 `claude -p` subprocess로 호출한다.

#### 선택 C — 아무것도 안 함

자동으로 mock 응답 사용. 시연은 정상 진행 (전 컴포넌트 작동).

#### 현재 상태 확인

```bash
curl http://localhost:8000/api/providers/status | python -m json.tool
```

응답 예:
```json
{
  "anthropic": {
    "model": "claude-sonnet-4-5",
    "api_key_present": ["ANTHROPIC_API_KEY"],
    "cli_available": true,
    "preferred_path": "api"
  },
  "openai": {
    "model": "gpt-4o-mini",
    "api_key_present": [],
    "cli_available": true,
    "preferred_path": "cli"
  }
}
```

### 2) Python 의존성 설치 + 서버 기동

Windows 에서는 루트에서 바로 실행 가능:

```powershell
.\RUN_DEMO.ps1
```

수동 실행:

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3) 브라우저 열기

http://localhost:8000

"박영희 ELS 가입 시도 → Advocate 발동" 버튼 → 5위험 체크 → 가입 → 송금 실행

## API 엔드포인트

| Method | Path | 설명 |
|---|---|---|
| GET | `/` | 정적 프론트엔드 (좌우 분할 UI) |
| GET | `/.well-known/agent.json` | OCP Agent Card |
| POST | `/api/review` | Seller·Advocate 1회 병렬 호출 + Z3 + Moderator + OCP audit |
| POST | `/api/review_mad?rounds=N` | **MAD 토론 모드** — N 라운드 cross-context embedding + Moderator 합의 |
| POST | `/api/fds/check` | 송금 단계 FDS + Family Consent |
| GET | `/api/audit/recent?limit=20` | OCP audit trail 최근 N건 |

### curl 예시

```bash
# 1) 리뷰 호출
curl -s -X POST http://localhost:8000/api/review \
  -H "content-type: application/json" \
  -d '{"customer_id":"park_younghee_75","product_id":"els_hongkong_h_2026_05"}' \
  | python -m json.tool

# 2) FDS 호출 (송금 시도)
curl -s -X POST http://localhost:8000/api/fds/check \
  -H "content-type: application/json" \
  -d '{"customer_id":"park_younghee_75","amount_krw":15000000}' \
  | python -m json.tool

# 3) Agent Card 조회
curl -s http://localhost:8000/.well-known/agent.json | python -m json.tool

# 4) audit trail
curl -s http://localhost:8000/api/audit/recent | python -m json.tool
```

## 파일 구조

```
woori-advocate/
├── README.md
├── backend/
│   ├── main.py              FastAPI 라우터
│   ├── agents.py            Seller·Advocate·Moderator (claude-agent-sdk)
│   ├── z3_verifier.py       Z3 SMT 금소법 §21·§22 형식 검증
│   ├── fds_family.py        FDS + Family Consent 룰 기반
│   ├── ocp_audit.py         OCP audit log + Agent Card
│   ├── requirements.txt
│   └── data/
│       ├── park_younghee_75.json   고객 mock
│       ├── els_hongkong_h.json     상품 mock
│       ├── els_terms_chunks.json   약관 RAG 청크 mock
│       ├── fscma_kb.json           금소법 6대 의무 KB
│       └── ocp_audit.log.jsonl     audit trail (실행 시 생성)
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── scenarios/
    └── scenario_0_integrated.md    12분 시연 timeline
```

## LLM Provider 폴백 매트릭스 (ZeroClaw 차용)

| Agent | Provider | 1순위 (API) | 2순위 (CLI) | 3순위 (Mock) | 데모 모드 |
|---|---|---|---|---|---|
| Seller | `anthropic` | `ANTHROPIC_API_KEY` → REST `messages` | `claude -p` subprocess (`~/.claude/`) | `MOCK_SELLER_RESPONSE` | `demo_cache/scenario_0_seller.txt` |
| Advocate | `openai` | `OPENAI_API_KEY` → REST `chat/completions` | `codex exec` subprocess (`~/.codex/`) | `MOCK_ADVOCATE_RESPONSE` | `demo_cache/scenario_0_advocate.json` |

응답 JSON 의 `seller.backend` / `advocate.backend` 필드로 어느 경로가 실제로 작동했는지 즉시 확인. 가능한 값:
- `anthropic-api` · `openai-api` — API key REST
- `claude-cli` · `codex-cli` — CLI OAuth
- `mock` · `mock-fallback` — 폴백
- `demo-cache` — 사전 캐시 (시연 모드)

`/api/providers/status` 엔드포인트로 사전 진단 가능 + 프론트엔드 상단 badge 에 실시간 표시.

### 시연 모드 (인터넷 장애·LLM 지연 대비)

본선 환경에서 인터넷 불안정 또는 LLM 지연 우려 시:

```bash
export WOORI_DEMO_MODE=cache   # 또는 Windows: set WOORI_DEMO_MODE=cache
uvicorn main:app --port 8000
```

`backend/data/demo_cache/` 의 사전 녹화 응답을 즉시 반환 (< 100ms). 응답 JSON 의 `backend: "demo-cache"` 로 캐시 사용 여부 가시화.

## 알려진 한계

- 본 PoC 의 이질 LLM 다양성은 system_prompt 격리만으로 시연 — `ClaudeAgentOptions(model=...)` 다중 호출은 grand design Phase 1.
- RAG 검색은 mock 청크 정적 주입 — Chroma·임베딩은 Phase 1.
- 감정 분석(민원 예방) 미포함 — Phase 2.
- 고객측 AI 협상은 Agent Card 노출만으로 시연 — 실 호출은 Phase 3.
- FDS 모델은 룰 기반 — GNN+transformer 는 Phase 2.

## 발표 자료 (docs/)

| 파일 | 설명 |
|---|---|
| [docs/woori_advocate_v1.pptx](docs/woori_advocate_v1.pptx) | **본선 PT용 16장 PPT** (16:9, 한국어, 우리 색) — S6 신규 "MAD vs LangGraph" 비교 포함 |
| [docs/presentation_guide.md](docs/presentation_guide.md) | **발표 가이드** — 슬라이드별 narration · 12분 시연 timeline · Q&A 30개 · 백업 계획 · 운영 체크리스트 |
| [docs/build_pptx.py](docs/build_pptx.py) | PPT 재생성 스크립트 (`python build_pptx.py`) |
| [docs/qa_pptx.py](docs/qa_pptx.py) | PPT 콘텐츠 QA (`python qa_pptx.py`) |
| [docs/render_to_images.py](docs/render_to_images.py) | PPT → PNG 시각 QA (`python render_to_images.py`) |
| [docs/slides_png/](docs/slides_png/) | PPT 슬라이드 PNG (15장, 시각 QA 검증용) |
| [docs/demo_recording/](docs/demo_recording/) | **라이브 데모 스크린샷 (4장)** — 01 초기 · 02 듀얼 · 02b 시니어 · 03 FDS+가족동의 |
| [docs/e2e_qa.py](docs/e2e_qa.py) | E2E 통합 QA (`python e2e_qa.py` — 서버 기동 후) |

### PPT 재빌드

```bash
cd docs
pip install python-pptx
python build_pptx.py    # → woori_advocate_v1.pptx (16장)
python qa_pptx.py       # 콘텐츠 검증 (16장 + 키워드 + speaker notes)
```

## 관련 문서

- 미션 정의: [.omc/autoresearch/woori-advocate-grand-design/mission.md](../.omc/autoresearch/woori-advocate-grand-design/mission.md)
- 그랜드 디자인 최종(113/120 PASS): [iter-0004-design.md](../.omc/autoresearch/woori-advocate-grand-design/runs/run-001/iterations/iter-0004-design.md)
- 원안 아이디어: [../아이디어/아이디어 1.md](../아이디어/아이디어%201.md)
- 컨테스트 공지: [../조사/공지.md](../조사/공지.md)
