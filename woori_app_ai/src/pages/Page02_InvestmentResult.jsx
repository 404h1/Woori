import { useState, useEffect } from 'react';
import StatusBar from '../components/StatusBar';
import VoiceGuide from '../components/VoiceGuide';

const SCRIPT = '결과 나왔어요. 고객님은 공격투자형이에요. 수익이 높은 대신 위험도 있는 상품에 적합한 성향이에요. 아래 확인 누르시면 맞는 펀드 보여드릴게요.';

export default function Page02_InvestmentResult({ onNext, onBack }) {
  const [animated, setAnimated] = useState(false);
  const [showVoice, setShowVoice] = useState(true);
  useEffect(() => {
    const timer = setTimeout(() => setAnimated(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const types = ['안정형', '안정\n추구형', '위험\n중립형', '적극\n투자형', '공격\n투자형'];

  return (
    <div className="phone-frame">
      <StatusBar />
      <div className="app-header">
        <button className="back-btn" onClick={onBack} style={{ position: 'absolute', left: 4, zIndex: 100, padding: 12, cursor: 'pointer', background: 'transparent', border: 'none' }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>
        <h1>투자성향분석 결과</h1>
        <button className="right-icon" style={{ color: '#888', fontSize: 16 }}>↓</button>
      </div>

      <div className="scroll-content" style={{ padding: '28px 20px 100px' }}>
        <div style={{ fontSize: 26, fontWeight: 700, color: '#111', lineHeight: 1.35, marginBottom: 16 }}>
          이혜원님의 투자성향은<br />
          <span style={{ color: '#dc2626' }}>공격투자형</span>입니다.
        </div>

        <div style={{ fontSize: 13, color: '#888', marginBottom: 20 }}>
          투자성향분석일: 2026.05.21
        </div>

        <div style={{ fontSize: 14, color: '#444', lineHeight: 1.7, marginBottom: 32 }}>
          시장평균 수익률을 훨씬 넘어서는 높은 수준의 투자수익을
          추구하며, 이를 위해 자산가치의 변동에 따른 손실 위험을
          적극 수용, 투자자금 대부분을 주식, 주식형펀드 또는 파생
          상품 등의 위험자산에 투자할 의향이 있음
        </div>

        {/* 투자성향 차트 */}
        <div style={{
          background: '#f8fafc', borderRadius: 16, padding: '20px 16px 16px',
          marginBottom: 32,
        }}>
          <div style={{ fontSize: 12, color: '#888', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 4 }}>
            ↑ 기대수익률
          </div>
          <div style={{ display: 'flex', gap: 6, alignItems: 'flex-end', marginBottom: 12, height: 96 }}>
            {types.map((t, i) => (
              <div key={i} style={{
                flex: 1,
                background: i === 4 ? '#dc2626' : '#e5e7eb',
                borderRadius: 10,
                height: animated ? (40 + i * 14) : 0,
                transition: 'height 0.8s cubic-bezier(0.25, 1, 0.5, 1)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                position: 'relative',
                overflow: 'hidden'
              }}>
                <div style={{
                  fontSize: 11, fontWeight: i === 4 ? 700 : 400,
                  color: i === 4 ? '#fff' : '#555',
                  whiteSpace: 'pre-wrap', textAlign: 'center',
                  lineHeight: 1.3,
                  flexShrink: 0
                }}>
                  {t}
                </div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 12, color: '#888', textAlign: 'right' }}>위험도 →</div>
        </div>

        {/* 안내 박스 */}
        <div style={{
          background: '#f8fafc', borderRadius: 12, padding: '16px',
          border: '1px solid #e5e7eb', marginBottom: 20,
        }}>
          <div style={{ fontSize: 13, color: '#444', lineHeight: 1.7, marginBottom: 12, display: 'flex', gap: 6 }}>
            <span style={{ color: '#1b64da', flexShrink: 0 }}>ℹ</span>
            <strong>단, 다음의 경우 설문항목의 답변에 따라 총점 상관없이 성향이 자동분류됩니다.</strong>
          </div>
          {[
            '투자원금이 보전되어야 하는 경우 (7번 질문 4번 답변, 10번 질문 3번 답변, 11번 질문 1번 답변) → 안정형',
            '투자기간이 1년 미만인 경우 (12번 질문 5번 답변) → 안정형',
            '사용예정자금(전세금, 임대차보증금) 단기운용인 경우 (9번 질문 4번 답변) → 위험중립형 이하',
          ].map((text, i) => (
            <div key={i} style={{ fontSize: 13, color: '#555', lineHeight: 1.7, paddingLeft: 8 }}>
              {i + 1}. {text}
            </div>
          ))}
        </div>
      </div>

      {/* 하단 버튼 */}
      <div style={{ padding: '12px 20px 24px', background: '#fff', flexShrink: 0 }}>
        <button className="btn-primary" onClick={onNext}>확인</button>
      </div>

      {!showVoice && (
        <button className="voice-fab" onClick={() => setShowVoice(true)}>🔊</button>
      )}
      {showVoice && (
        <VoiceGuide
          script={SCRIPT}
          onClose={() => setShowVoice(false)}
          onCommand={(cmd) => {
            if (cmd.includes('확인') || cmd.includes('다음')) onNext();
          }}
        />
      )}
    </div>
  );
}
