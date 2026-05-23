import { useState } from 'react';
import StatusBar from '../components/StatusBar';
import VoiceGuide from '../components/VoiceGuide';


const SCRIPT = '솔직하게 말씀드릴게요. 이 펀드, 엔비디아 TSMC 같은 AI 반도체 기업들에 투자하는 거라 요즘 수익률이 엄청 높아요. 근데 고객님 상황에서 한 가지 짚어드리고 싶은 게 있어요. 지금 비상금이 따로 없으시잖아요. 이 펀드는 중간에 빼면 수수료에 손실까지 날 수 있어요. 그러니까 이렇게 하세요. 25일 급여 들어오면 20만원은 비상금으로 무조건 빼두시고, 나머지 10만원으로 시작해보세요. 처음 투자니까 소액으로 감 잡는 게 맞아요.';

const PROS = [
  { icon: '📈', title: '높은 수익 잠재력', desc: 'AI 반도체 수요 급증으로 최근 3개월 +46% 달성' },
  { icon: '🌐', title: '글로벌 분산 투자', desc: '엔비디아·TSMC·삼성전자 등 세계 TOP 기업에 분산' },
  { icon: '💡', title: '성장 테마 직접 투자', desc: 'AI·데이터센터 핵심 인프라 반도체에 집중 투자' },
];

const CONS = [
  { icon: '⚠️', title: '높은 변동성', desc: '반도체 업황에 따라 수익률이 크게 오르내릴 수 있어요' },
  { icon: '💸', title: '원금 손실 가능', desc: '예금자보호 대상 아님, 투자 원금 일부·전부 손실 가능해요' },
  { icon: '🔄', title: '환율 리스크', desc: '해외 주식 투자라 환율 변동에 따른 추가 손익이 생겨요' },
];

const FIT = [
  { ok: true,  label: '5년 이상 장기 투자 가능하신 분' },
  { ok: true,  label: '원금 손실을 감수하고 높은 수익을 원하시는 분' },
  { ok: true,  label: 'AI·반도체 성장에 확신이 있으신 분' },
  { ok: false, label: '1~2년 내 자금이 필요하신 분' },
  { ok: false, label: '원금 보장이 필요하신 분' },
];

export default function Page03c_FundAI({ onBack, onJoin }) {
  const [tab, setTab] = useState('pros');
  const [showVoice, setShowVoice] = useState(true);

  return (
    <div className="phone-frame">
      <StatusBar />
      <div className="app-header">
        <button className="back-btn" onClick={onBack} style={{ position: 'absolute', left: 4, zIndex: 100, padding: 12, cursor: 'pointer', background: 'transparent', border: 'none' }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>
        <h1>AI 펀드 설명</h1>
      </div>

      <div className="scroll-content" style={{ paddingBottom: 100 }}>

        {/* 펀드명 */}
        <div style={{ padding: '20px 20px 0', background: 'linear-gradient(180deg,#eef4ff 0%,#fff 100%)' }}>
          <div style={{ fontSize: 12, color: '#888', marginBottom: 4 }}>삼성글로벌반도체증권자투자신탁UH[주식]Ae</div>
          <div style={{ fontSize: 20, fontWeight: 800, color: '#111', marginBottom: 16 }}>글로벌 반도체 기업 투자하기</div>
        </div>

        {/* 탭 */}
        <div style={{ display: 'flex', borderBottom: '1px solid #f0f2f5', margin: '0 20px' }}>
          {[['pros','👍 장점'],['cons','⚠️ 주의'],['fit','👤 적합한 분']].map(([key, label]) => (
            <button key={key} onClick={() => setTab(key)} style={{
              flex: 1, padding: '12px 0', fontSize: 13,
              fontWeight: tab === key ? 700 : 400,
              color: tab === key ? '#1b64da' : '#888',
              background: 'none', border: 'none',
              borderBottom: tab === key ? '2px solid #1b64da' : '2px solid transparent',
              cursor: 'pointer',
            }}>
              {label}
            </button>
          ))}
        </div>

        <div style={{ padding: '20px' }}>
          {tab === 'pros' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {PROS.map((item, i) => (
                <div key={i} style={{ background: '#f0f7ff', borderRadius: 14, padding: '16px', display: 'flex', gap: 14 }}>
                  <span style={{ fontSize: 24, flexShrink: 0 }}>{item.icon}</span>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: '#111', marginBottom: 4 }}>{item.title}</div>
                    <div style={{ fontSize: 13, color: '#555', lineHeight: 1.6 }}>{item.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {tab === 'cons' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {CONS.map((item, i) => (
                <div key={i} style={{ background: '#fff5f5', borderRadius: 14, padding: '16px', display: 'flex', gap: 14 }}>
                  <span style={{ fontSize: 24, flexShrink: 0 }}>{item.icon}</span>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: '#dc2626', marginBottom: 4 }}>{item.title}</div>
                    <div style={{ fontSize: 13, color: '#555', lineHeight: 1.6 }}>{item.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {tab === 'fit' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {FIT.map((item, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '14px 16px', background: item.ok ? '#f0fff4' : '#fff5f5', borderRadius: 12 }}>
                  <span style={{ fontSize: 18 }}>{item.ok ? '✅' : '❌'}</span>
                  <span style={{ fontSize: 14, color: '#222', lineHeight: 1.5 }}>{item.label}</span>
                </div>
              ))}
            </div>
          )}

          {/* ── 고객 맞춤 조언 카드 ── */}
          <div style={{ marginTop: 24, background: '#fff', border: '1.5px solid #1b64da', borderRadius: 16, overflow: 'hidden' }}>
            <div style={{ background: '#1b64da', padding: '12px 16px', display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: 16 }}>💬</span>
              <span style={{ fontSize: 14, fontWeight: 700, color: '#fff' }}>이혜원 고객님 맞춤 조언</span>
            </div>

            <div style={{ padding: '16px' }}>
              {/* 자금 분석 */}
              {[
                { label: '월 여유자금', value: '300,000원', color: '#111' },
                { label: '권장 비상금', value: '- 200,000원', color: '#dc2626' },
              ].map(({ label, value, color }) => (
                <div key={label} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #f0f2f5' }}>
                  <span style={{ fontSize: 14, color: '#666' }}>{label}</span>
                  <span style={{ fontSize: 14, fontWeight: 600, color }}>{value}</span>
                </div>
              ))}
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', marginBottom: 12 }}>
                <span style={{ fontSize: 15, fontWeight: 700, color: '#111' }}>추천 투자금액</span>
                <span style={{ fontSize: 15, fontWeight: 800, color: '#1b64da' }}>100,000원 ✅</span>
              </div>

              <div style={{ background: '#f0f7ff', borderRadius: 10, padding: '12px 14px', marginBottom: 16 }}>
                <p style={{ fontSize: 13, color: '#1b64da', lineHeight: 1.7, margin: 0 }}>
                  "처음 투자니까 소액으로 감 잡는 게 맞아요. 25일 급여 들어오시면 비상금 20만원 먼저 빼두시고, 나머지 10만원으로 시작해보세요."
                </p>
              </div>

              <button
                onClick={onJoin}
                style={{ width: '100%', background: '#1b64da', color: '#fff', border: 'none', borderRadius: 12, padding: '14px', fontSize: 15, fontWeight: 700, cursor: 'pointer' }}
              >
                10만원으로 바로 가입하기
              </button>
            </div>
          </div>
        </div>
      </div>

      <div style={{ padding: '12px 20px 24px', background: '#fff', flexShrink: 0 }}>
        <button className="btn-primary" onClick={onJoin}>가입하기</button>
      </div>

      {!showVoice && (
        <button className="voice-fab" onClick={() => setShowVoice(true)}>🔊</button>
      )}
      {showVoice && (
        <VoiceGuide
          script={SCRIPT}
          onClose={() => setShowVoice(false)}
          onCommand={(cmd) => {
            if (cmd.includes('가입') || cmd.includes('시작')) onJoin();
          }}
        />
      )}
    </div>
  );
}
