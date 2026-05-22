import { useState } from 'react';
import StatusBar from '../components/StatusBar';

const FUNDS = [
  { id: 1, risk: '매우높은위험', riskClass: 'tag-red', extra: '원금손실가능', name: '미래에셋코어테크증권자투자신탁(주식)A-e', region: '국내', fee: '수수료선취', channel: '온라인', return3m: '+46.27%' },
  { id: 2, risk: '매우높은위험', riskClass: 'tag-red', extra: '원금손실가능', name: '미래에셋코어테크증권자투자신탁(주식)C-e', region: '국내', fee: '수수료미징구', channel: '온라인', return3m: '+46.27%' },
  { id: 3, risk: '매우높은위험', riskClass: 'tag-red', extra: '원금손실가능', name: '삼성글로벌반도체증권자투자신탁UH[주식]Ae', region: '글로벌', fee: '수수료선취', channel: '온라인', return3m: '+46.54%' },
  { id: 4, risk: '매우높은위험', riskClass: 'tag-red', extra: '원금손실가능', name: '삼성글로벌반도체증권자투자신탁UH[주식]Ce', region: '글로벌', fee: '수수료미징구', channel: '온라인', return3m: '+46.47%' },
  { id: 5, risk: '매우높은위험', riskClass: 'tag-red', extra: '원금손실가능', name: '한국투자테크증권자투자신탁1호(주식)A-e', region: '국내', fee: '수수료선취', channel: '온라인', return3m: '+44.35%' },
  { id: 6, risk: '매우높은위험', riskClass: 'tag-red', extra: '원금손실가능', name: '한국투자테크증권자투자신탁1호(주식)C-e', region: '국내', fee: '수수료미징구', channel: '온라인', return3m: '+44.12%' },
  { id: 7, risk: '높은위험', riskClass: 'tag-orange', extra: '원금손실가능', name: '우리삼성그룹증권자투자신탁1호[주식]A-e', region: '국내', fee: '계열사·수수료선취', channel: '온라인', return3m: '+38.83%' },
  { id: 8, risk: '높은위험', riskClass: 'tag-orange', extra: '원금손실가능', name: '우리삼성그룹증권자투자신탁1호[주식]C-e', region: '국내', fee: '계열사·수수료미징구', channel: '온라인', return3m: '+38.78%' },
  { id: 9, risk: '매우높은위험', riskClass: 'tag-red', extra: '원금손실가능', name: '한화그린히어로증권자투자신탁(주식)A-e', region: '글로벌', fee: '수수료선취', channel: '온라인', return3m: '+37.84%' },
];

export default function Page03_FundList({ onNext, onFundDetail }) {
  const [selected, setSelected] = useState([]);

  const toggleSelect = (fund) => {
    setSelected(prev => {
      const exists = prev.find(f => f.id === fund.id);
      if (exists) return prev.filter(f => f.id !== fund.id);
      if (prev.length >= 2) return prev;
      return [...prev, fund];
    });
  };

  const isSelected = (id) => selected.some(f => f.id === id);

  return (
    <div className="phone-frame">
      <StatusBar />
      <div className="app-header">
        <button className="back-btn">〈</button>
        <h1>수익률 BEST</h1>
        <button className="right-icon">🛍</button>
      </div>

      <div className="scroll-content" style={{ paddingBottom: selected.length > 0 ? 120 : 20 }}>
        {/* 투자성향 배너 */}
        <div style={{ padding: '16px 20px', borderBottom: '1px solid #f0f2f5' }}>
          <div style={{ fontSize: 14, color: '#222', lineHeight: 1.6, marginBottom: 6 }}>
            고객님의 투자성향은 <strong style={{ color: '#dc2626' }}>공격투자형</strong>입니다.<br />
            <span style={{ color: '#dc2626', fontWeight: 600 }}>매우높은위험</span> 등급 이하의 상품만 조회됩니다.
          </div>
          <div style={{ fontSize: 12, color: '#888', lineHeight: 1.6 }}>
            ※ 과거수익률이 미래수익률을 보장하지 않습니다.<br />
            ※ 이 금융상품은 예금자보호법에 따라 보호되지 않습니다.
          </div>
        </div>

        {/* 펀드 목록 */}
        <div style={{ padding: '12px 16px', display: 'flex', flexDirection: 'column', gap: 12 }}>
          {FUNDS.map(fund => (
            <div
              key={fund.id}
              onClick={() => fund.id === 3 && onFundDetail && onFundDetail()}
              style={{
                background: '#fff',
                border: isSelected(fund.id) ? '2px solid #1b64da' : '1.5px solid #e5e7eb',
                borderRadius: 14,
                padding: '16px',
                cursor: 'pointer',
              }}
            >
              <div style={{ display: 'flex', gap: 6, marginBottom: 8 }}>
                <span className={`tag ${fund.riskClass}`}>{fund.risk}</span>
                <span className="tag tag-pink">{fund.extra}</span>
              </div>
              <div style={{ fontSize: 14, fontWeight: 700, color: '#111', marginBottom: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                {fund.name}
                <span style={{ fontSize: 18, color: '#999', flexShrink: 0, marginLeft: 4 }}>›</span>
              </div>
              <div style={{ fontSize: 12, color: '#888', marginBottom: 12 }}>
                {fund.region} | {fund.fee} | {fund.channel}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <button
                  onClick={(e) => { e.stopPropagation(); toggleSelect(fund); }}
                  style={{
                    background: isSelected(fund.id) ? '#1b64da' : '#f2f4f6',
                    color: isSelected(fund.id) ? '#fff' : '#555',
                    border: 'none', borderRadius: 20,
                    padding: '7px 16px', fontSize: 13, fontWeight: 600,
                    cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 4,
                  }}
                >
                  {isSelected(fund.id) ? '✓ 비교담기' : '∨ 비교담기'}
                </button>
                <div style={{ fontSize: 13, color: '#555' }}>
                  3개월 수익률 <strong style={{ color: '#dc2626' }}>{fund.return3m}</strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 하단 비교 바 */}
      {selected.length > 0 && (
        <div style={{
          position: 'absolute', bottom: 0, left: 0, right: 0,
          background: '#fff', borderTop: '1px solid #f0f2f5',
          padding: '12px 16px 24px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
            <span style={{ fontSize: 14, fontWeight: 700 }}>
              선택된 상품 <span style={{ color: '#1b64da' }}>{selected.length}개</span>
            </span>
            {selected.length === 2 && (
              <button
                onClick={onNext}
                style={{
                  background: '#1b64da', color: '#fff', border: 'none',
                  borderRadius: 20, padding: '8px 20px',
                  fontSize: 14, fontWeight: 700, cursor: 'pointer',
                }}
              >
                비교하기
              </button>
            )}
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            {selected.map(f => (
              <div key={f.id} style={{
                background: '#f2f4f6', borderRadius: 20, padding: '6px 12px',
                fontSize: 12, color: '#333', display: 'flex', alignItems: 'center', gap: 6,
                maxWidth: '45%', overflow: 'hidden',
              }}>
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {f.name.slice(0, 10)}...
                </span>
                <button onClick={() => toggleSelect(f)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#888', fontSize: 14, flexShrink: 0 }}>×</button>
              </div>
            ))}
            {selected.length < 2 && (
              <div style={{
                background: '#f2f4f6', borderRadius: 20, padding: '6px 16px',
                fontSize: 12, color: '#aaa',
              }}>
                추가하기
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
