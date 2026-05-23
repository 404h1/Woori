import { useState } from 'react';
import StatusBar from '../components/StatusBar';
import BotAvatar from '../components/BotAvatar';
import VoiceGuide from '../components/VoiceGuide';

const SCRIPT = 'AI가 이 펀드를 쉽게 설명해 드릴게요. 삼성 글로벌 반도체 펀드는 엔비디아, TSMC, 삼성전자처럼 전 세계 유명 반도체 기업에 투자해요. AI 열풍으로 반도체 수요가 폭발적으로 늘면서 최근 수익률이 아주 높아요. 다만 반도체 업황에 따라 크게 오르내릴 수 있고 원금 손실 가능성이 있어요. 공격적 투자 성향의 고객님께 잘 맞는 상품이에요.';

const PROS = [
  { icon: '📈', title: '높은 수익 잠재력', desc: 'AI 반도체 수요 급증으로 최근 3개월 +46% 달성' },
  { icon: '🌐', title: '글로벌 분산 투자', desc: '엔비디아·TSMC·삼성전자 등 세계 TOP 기업에 분산' },
  { icon: '💡', title: '성장 테마 직접 투자', desc: 'AI·데이터센터 핵심 인프라 반도체에 집중 투자' },
];

const CONS = [
  { icon: '⚠️', title: '높은 변동성', desc: '반도체 업황에 따라 수익률이 크게 오르내릴 수 있음' },
  { icon: '💸', title: '원금 손실 가능', desc: '예금자보호 대상 아님, 투자 원금 일부·전부 손실 가능' },
  { icon: '🔄', title: '환율 리스크', desc: '해외 주식 투자로 환율 변동에 따른 추가 손익 발생 가능' },
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
        <h1>내 편인 AI 설명</h1>
      </div>

      <div className="scroll-content" style={{ paddingBottom: 100 }}>
        {/* AI 헤더 */}
        <div style={{ padding: '20px 20px 0', background: 'linear-gradient(180deg, #eef4ff 0%, #fff 100%)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
            <BotAvatar size={48} />
            <div>
              <div style={{ fontSize: 13, fontWeight: 700, color: '#1b64da', marginBottom: 2 }}>내 편인 AI</div>
              <div style={{ fontSize: 12, color: '#888' }}>삼성 글로벌 반도체 펀드 분석</div>
            </div>
          </div>

          {/* AI 버블 */}
          <div style={{ background: '#f2f4f6', borderRadius: '4px 16px 16px 16px', padding: '14px 16px', marginBottom: 20 }}>
            <p style={{ fontSize: 14, color: '#222', lineHeight: 1.7 }}>
              안녕하세요, 이혜원 고객님! 👋<br />
              이 펀드에 대해 쉽게 설명해 드릴게요.<br /><br />
              <strong>엔비디아, TSMC, 삼성전자</strong> 같은 글로벌 반도체 기업들에 투자하는 펀드예요. AI 열풍으로 반도체 수요가 폭발하면서 최근 수익률이 아주 높아요. 🚀
            </p>
          </div>
        </div>

        {/* 탭 */}
        <div style={{ display: 'flex', borderBottom: '1px solid #f0f2f5', margin: '0 20px' }}>
          {[['pros', '👍 장점'], ['cons', '⚠️ 주의할 점'], ['fit', '👤 이런 분께']].map(([key, label]) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              style={{
                flex: 1, padding: '12px 0', fontSize: 13, fontWeight: tab === key ? 700 : 400,
                color: tab === key ? '#1b64da' : '#888', background: 'none', border: 'none',
                borderBottom: tab === key ? '2px solid #1b64da' : '2px solid transparent',
                cursor: 'pointer', transition: 'all 0.15s',
              }}
            >
              {label}
            </button>
          ))}
        </div>

        <div style={{ padding: '20px 20px 0' }}>
          {tab === 'pros' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {PROS.map((item, i) => (
                <div key={i} className="bubble-in" style={{ animationDelay: `${i * 0.08}s`, background: '#f0f7ff', borderRadius: 14, padding: '16px', display: 'flex', gap: 14, alignItems: 'flex-start' }}>
                  <div style={{ fontSize: 24, flexShrink: 0 }}>{item.icon}</div>
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
                <div key={i} className="bubble-in" style={{ animationDelay: `${i * 0.08}s`, background: '#fff5f5', borderRadius: 14, padding: '16px', display: 'flex', gap: 14, alignItems: 'flex-start' }}>
                  <div style={{ fontSize: 24, flexShrink: 0 }}>{item.icon}</div>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: '#dc2626', marginBottom: 4 }}>{item.title}</div>
                    <div style={{ fontSize: 13, color: '#555', lineHeight: 1.6 }}>{item.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {tab === 'fit' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {[
                { icon: '✅', label: '5년 이상 장기 투자 가능하신 분' },
                { icon: '✅', label: '원금 손실을 감수하고 높은 수익을 원하시는 분' },
                { icon: '✅', label: 'AI·반도체 성장에 확신이 있으신 분' },
                { icon: '❌', label: '1~2년 내 자금이 필요하신 분' },
                { icon: '❌', label: '원금 보장이 필요하신 분' },
              ].map((item, i) => (
                <div key={i} className="bubble-in" style={{ animationDelay: `${i * 0.07}s`, display: 'flex', alignItems: 'center', gap: 12, padding: '14px 16px', background: item.icon === '✅' ? '#f0fff4' : '#fff5f5', borderRadius: 12 }}>
                  <span style={{ fontSize: 20 }}>{item.icon}</span>
                  <span style={{ fontSize: 14, color: '#222', lineHeight: 1.5 }}>{item.label}</span>
                </div>
              ))}

              <div style={{ marginTop: 4, padding: '14px 16px', background: '#eef4ff', borderRadius: 12, display: 'flex', gap: 10, alignItems: 'flex-start' }}>
                <BotAvatar size={28} />
                <p style={{ fontSize: 13, color: '#1b64da', lineHeight: 1.6 }}>
                  고객님은 <strong>공격투자형</strong>으로 이 펀드에 적합한 성향이에요. 다만 투자 금액의 일부만 배분하는 것을 추천해요. 😊
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      <div style={{ padding: '12px 20px 24px', background: '#fff', flexShrink: 0 }}>
        <button className="btn-primary" onClick={onJoin}>이 펀드 가입하기</button>
      </div>

      {!showVoice && (
        <button className="voice-fab" onClick={() => setShowVoice(true)}>🔊</button>
      )}
      {showVoice && (
        <VoiceGuide
          script={SCRIPT}
          onClose={() => setShowVoice(false)}
          onCommand={(cmd) => {
            if (cmd.includes('가입')) onJoin?.();
            else if (cmd.includes('장점')) setTab('pros');
            else if (cmd.includes('단점') || cmd.includes('주의')) setTab('cons');
            else if (cmd.includes('뒤') || cmd.includes('이전')) onBack();
          }}
        />
      )}
    </div>
  );
}
