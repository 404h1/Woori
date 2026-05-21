/*
 * Woori Advocate frontend
 *
 * 1. /api/review 호출 → 좌(Seller) 우(Advocate) 분할 출력
 * 2. Advocate 위험 항목 N개 모두 체크해야 "가입 진행" 버튼 활성
 * 3. 가입 완료 → 송금 단계 → /api/fds/check 호출 → 통합 시나리오 0 데모
 * 4. OCP audit trail 표시
 */

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

const state = {
  acknowledged: new Set(),
  totalItems: 0,
  senior: false,
  ttsAvailable: typeof window !== "undefined" && "speechSynthesis" in window,
};

function setSenior(enabled) {
  state.senior = enabled;
  document.body.classList.toggle("senior", enabled);
}

function speak(text) {
  if (!state.senior || !state.ttsAvailable) return;
  try {
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = "ko-KR";
    utt.rate = 0.95;
    window.speechSynthesis.speak(utt);
  } catch (e) {
    console.warn("TTS failed", e);
  }
}

function renderSeller(seller) {
  $("#seller-body").textContent = seller.text;
  $("#seller-backend").textContent = `${seller.backend} · ${seller.model_hint || ""}`;
}

function renderZ3(proof) {
  const badge = $("#z3-badge");
  badge.classList.remove("good", "bad");
  if (proof.all_passed) {
    badge.classList.add("good");
    badge.textContent = `Z3 SMT ✓ 금소법 §21·§22 검증 통과 (${proof.kb_version})`;
  } else {
    badge.classList.add("bad");
    const matched = proof.results
      .filter((r) => !r.passed)
      .flatMap((r) => r.matched_patterns)
      .join(", ");
    badge.textContent = `Z3 SMT ✗ 부당권유 패턴 검출: ${matched}`;
  }
}

function renderAdvocate(customer, advocate) {
  $("#advocate-customer").textContent =
    `${customer.name}님 (${customer.age}세) — ` +
    `가입 서명 전에 이 상품이 맞지 않을 수 있는 ${advocate.items.length}가지 이유를 확인해 주세요.`;
  $("#advocate-backend").textContent = `${advocate.backend} · ${advocate.model_hint || ""}`;

  const list = $("#advocate-list");
  list.innerHTML = "";
  state.acknowledged.clear();
  state.totalItems = advocate.items.length;

  advocate.items.forEach((item, idx) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="item-head">
        <span class="item-no">${item.no || idx + 1}.</span>
        <span class="item-title">${escapeHtml(item.title || "")}</span>
        <span class="item-source">출처 ${escapeHtml(item.source || "n/a")}</span>
      </div>
      <div class="item-body">${escapeHtml(item.explanation || "")}</div>
      <label class="item-ack">
        <input type="checkbox" data-idx="${idx}">
        위 ${item.no || idx + 1}번 위험을 읽고 이해했습니다.
      </label>
    `;
    list.appendChild(li);
  });

  list.querySelectorAll("input[type=checkbox]").forEach((cb) => {
    cb.addEventListener("change", (e) => {
      const idx = e.target.getAttribute("data-idx");
      if (e.target.checked) state.acknowledged.add(idx);
      else state.acknowledged.delete(idx);
      updateGate();
    });
  });

  updateGate();

  // 시니어 모드면 첫 위험을 TTS 로 읽어줌
  if (state.senior && advocate.items[0]) {
    speak(
      `${customer.name}님, 첫 번째 위험을 안내해 드릴게요. ` +
        advocate.items[0].title +
        ". " +
        advocate.items[0].explanation
    );
  }
}

function updateGate() {
  const n = state.acknowledged.size;
  $("#check-progress").textContent = `${n}/${state.totalItems} 위험 인지`;
  $("#btn-sign").disabled = n < state.totalItems || state.totalItems === 0;
}

function renderAudit(audit, fullPayload) {
  $("#audit-panel").classList.remove("hidden");
  $("#audit-json").textContent = JSON.stringify({ audit, full: fullPayload }, null, 2);
}

function renderFDS(fds) {
  const el = $("#fds-output");
  el.classList.remove("hidden");
  const signals = fds.triggered_signals
    .map((s) => `<li>${escapeHtml(s)}</li>`)
    .join("");
  el.innerHTML = `
    <h3>FDS 평가
      <span class="recommendation-badge ${fds.recommendation}">${fds.recommendation}</span>
      <small>(risk_score=${fds.risk_score})</small>
    </h3>
    <ul class="signal-list">${signals}</ul>
    <small>${escapeHtml(fds.detail.note || "")}</small>
  `;
}

function renderFamily(family) {
  const el = $("#family-output");
  el.classList.remove("hidden");
  if (!family.required) {
    el.innerHTML = `<h3>가족 동의 절차 — 불필요</h3><small>FDS 가 PROCEED 판정</small>`;
    return;
  }
  const flow = family.flow.map((s) => `<li>${escapeHtml(s)}</li>`).join("");
  const contacts = family.contacts_to_verify
    .map((c) => `<li>${escapeHtml(c.name)} — ${escapeHtml(c.phone)}</li>`)
    .join("");
  el.innerHTML = `
    <h3>가족 동의 절차 — 발동</h3>
    <h4>확인 대상</h4>
    <ul class="signal-list">${contacts}</ul>
    <h4>절차</h4>
    <ol class="signal-list">${flow}</ol>
  `;
  if (state.senior) speak("이 송금은 가족 확인이 필요합니다. 손주에게 직접 전화로 확인해 주세요.");
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function loadProviderStatus() {
  try {
    const resp = await fetch("/api/providers/status");
    if (!resp.ok) return;
    const data = await resp.json();
    const badge = $("#provider-badge");
    const sellerPath = data.anthropic?.preferred_path || "?";
    const advocatePath = data.openai?.preferred_path || "?";
    $("#provider-seller").textContent = `Seller: ${sellerPath}`;
    $("#provider-advocate").textContent = `Advocate: ${advocatePath}`;
    // 가장 약한 경로로 색상 결정
    badge.classList.remove("api", "cli", "mock", "cache");
    const worst =
      [sellerPath, advocatePath].includes("mock") ? "mock"
      : [sellerPath, advocatePath].includes("cli") ? "cli"
      : "api";
    badge.classList.add(worst);
  } catch (e) {
    console.warn("provider status fetch failed", e);
  }
}

function showLoading(visible) {
  $("#loading-overlay").classList.toggle("hidden", !visible);
}

function toast(msg, kind = "info", ms = 3500) {
  const el = $("#toast");
  el.className = `toast ${kind}`;
  el.textContent = msg;
  el.classList.remove("hidden");
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => el.classList.add("hidden"), ms);
}

function resetDemo() {
  $("#split-view").classList.add("hidden");
  $("#mad-view").classList.add("hidden");
  $("#mad-rounds").innerHTML = "";
  $("#mad-consensus").classList.add("hidden");
  $("#transfer-step").classList.add("hidden");
  $("#audit-panel").classList.add("hidden");
  $("#fds-output")?.classList.add("hidden");
  $("#family-output")?.classList.add("hidden");
  $("#btn-reset").classList.add("hidden");
  $("#btn-review").disabled = false;
  $("#btn-mad").disabled = false;
  $("#btn-review").textContent = "박영희 ELS 가입 시도 → Advocate 발동";
  $("#btn-sign").disabled = true;
  state.acknowledged.clear();
  state.totalItems = 0;
  $("#senior-mode-toggle").checked = false;
  setSenior(false);
  toast("초기화 완료", "info", 1500);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderMadRounds(rounds) {
  const wrap = $("#mad-rounds");
  wrap.innerHTML = "";
  rounds.forEach((r, idx) => {
    const note = idx === 0
      ? "독립 호출 — 서로 못 봄 (Round 1 baseline)"
      : "직전 라운드 상대 출력을 system prompt context 에 embedding 후 재작성";
    const advItems = r.advocate.items.map(it =>
      `<li><strong>${escapeHtml(it.title || "")}</strong> <span class="item-source">${escapeHtml(it.source || "")}</span></li>`
    ).join("");
    const sellerHtml = escapeHtml(r.seller.text || "");
    const card = document.createElement("div");
    card.className = "mad-round";
    card.innerHTML = `
      <div class="mad-round-head">
        <span class="mad-round-num">Round ${r.round}</span>
        <span class="mad-round-note">${note}</span>
      </div>
      <div class="mad-round-body">
        <div class="mad-pane-seller">
          <div class="mad-pane-label">
            <span class="mad-pane-name">Seller (Claude)</span>
            <span class="mad-backend">${escapeHtml(r.seller.backend)}</span>
          </div>
          <div class="mad-pane-body">${sellerHtml}</div>
        </div>
        <div class="mad-pane-advocate">
          <div class="mad-pane-label">
            <span class="mad-pane-name">Advocate (GPT)</span>
            <span class="mad-backend">${escapeHtml(r.advocate.backend)}</span>
          </div>
          <div class="mad-pane-body"><ol>${advItems}</ol></div>
        </div>
      </div>
    `;
    wrap.appendChild(card);
    if (idx < rounds.length - 1) {
      const arrow = document.createElement("div");
      arrow.className = "mad-arrow";
      arrow.textContent = "↓ 상호 출력이 다음 라운드 context 에 embedding ↓";
      wrap.appendChild(arrow);
    }
  });
}

function renderMadConsensus(consensus) {
  const el = $("#mad-consensus");
  const agreed = (consensus.agreed || []).map(s => `<li>${escapeHtml(s)}</li>`).join("");
  const disagreed = (consensus.disagreed || []).map(s => `<li>${escapeHtml(s)}</li>`).join("");
  el.innerHTML = `
    <h3>
      Moderator 합의
      <span class="mad-verdict-badge ${escapeHtml(consensus.verdict || "balanced")}">${escapeHtml(consensus.verdict || "balanced")}</span>
    </h3>
    <div class="mad-consensus-grid">
      <div>
        <h4>합의 (agreed)</h4>
        <ul>${agreed || "<li><em>없음</em></li>"}</ul>
      </div>
      <div>
        <h4>불일치 (disagreed)</h4>
        <ul>${disagreed || "<li><em>없음</em></li>"}</ul>
      </div>
    </div>
  `;
  el.classList.remove("hidden");
}

// ─── Wire up ─────────────────────────────────────────────────────────────

$("#senior-mode-toggle").addEventListener("change", (e) => setSenior(e.target.checked));
$("#btn-reset").addEventListener("click", resetDemo);

$("#btn-mad").addEventListener("click", async () => {
  $("#btn-mad").disabled = true;
  $("#btn-review").disabled = true;
  showLoading(true);
  try {
    const resp = await fetch("/api/review_mad?rounds=2", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({}),
    });
    if (!resp.ok) throw new Error("review_mad API 실패: " + resp.status);
    const data = await resp.json();

    $("#mad-view").classList.remove("hidden");
    renderMadRounds(data.debate_rounds);
    renderMadConsensus(data.consensus);
    renderAudit(data.audit, data);
    $("#btn-reset").classList.remove("hidden");
    toast(`MAD 토론 완료 · ${data.debate_rounds.length} 라운드 · ${data.consensus.verdict}`,
          "success", 3500);
    $("#mad-view").scrollIntoView({ behavior: "smooth" });
  } catch (e) {
    toast("MAD 오류: " + e.message, "info", 4000);
  } finally {
    showLoading(false);
    $("#btn-mad").disabled = false;
    $("#btn-review").disabled = false;
  }
});

loadProviderStatus();

$("#btn-review").addEventListener("click", async () => {
  $("#btn-review").disabled = true;
  $("#btn-review").textContent = "Advocate 분석 중...";
  showLoading(true);
  try {
    const resp = await fetch("/api/review", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        customer_id: "park_younghee_75",
        product_id: "els_hongkong_h_2026_05",
      }),
    });
    if (!resp.ok) throw new Error("review API 실패: " + resp.status);
    const data = await resp.json();

    // 시니어 모드 자동 활성화
    if (data.customer.senior_mode && !state.senior) {
      $("#senior-mode-toggle").checked = true;
      setSenior(true);
    }

    $("#split-view").classList.remove("hidden");
    renderSeller(data.seller);
    renderZ3(data.formal_proof);
    renderAdvocate(data.customer, data.advocate);
    renderAudit(data.audit, data);
    $("#btn-reset").classList.remove("hidden");
    toast(`Seller=${data.seller.backend} · Advocate=${data.advocate.backend}`, "success", 2500);
  } catch (e) {
    toast("오류: " + e.message, "info", 4000);
  } finally {
    showLoading(false);
    $("#btn-review").disabled = false;
    $("#btn-review").textContent = "다시 실행";
  }
});

$("#btn-sign").addEventListener("click", () => {
  $("#transfer-step").classList.remove("hidden");
  $("#transfer-step").scrollIntoView({ behavior: "smooth" });
});

$("#btn-transfer").addEventListener("click", async () => {
  $("#btn-transfer").disabled = true;
  showLoading(true);
  try {
    const resp = await fetch("/api/fds/check", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        customer_id: "park_younghee_75",
        amount_krw: 15000000,
        recipient_name: "이주민 (자칭 손주)",
        recipient_account_age_days: 3,
        recipient_claimed_relation: "손주",
        recipient_actual_call_history_6m_count: 0,
      }),
    });
    if (!resp.ok) throw new Error("FDS API 실패: " + resp.status);
    const data = await resp.json();
    renderFDS(data.fds);
    renderFamily(data.family_consent);
    renderAudit(data.audit, data);
    toast(`FDS ${data.fds.recommendation} (risk=${data.fds.risk_score})`,
          data.fds.recommendation === "BLOCK" ? "info" : "success", 3000);
  } catch (e) {
    toast("오류: " + e.message, "info", 4000);
  } finally {
    showLoading(false);
    $("#btn-transfer").disabled = false;
  }
});
