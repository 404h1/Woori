import { useState, useRef } from 'react';
import StatusBar from '../components/StatusBar';

export default function Page07_Document({ onClose, onNext }) {
  const [scrolled, setScrolled] = useState(false);
  const scrollRef = useRef(null);

  const handleScroll = () => {
    const el = scrollRef.current;
    if (!el) return;
    const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 60;
    if (atBottom) setScrolled(true);
  };

  return (
    <div className="phone-frame">
      <StatusBar />
      <div className="app-header">
        <h1>집합투자상품설명서 확인</h1>
        <button onClick={onClose} style={{ position: 'absolute', right: 16, background: 'none', border: 'none', fontSize: 22, cursor: 'pointer', color: '#333' }}>✕</button>
      </div>

      <div
        ref={scrollRef}
        onScroll={handleScroll}
        className="scroll-content"
        style={{ padding: '20px 20px 100px' }}
      >
        {/* 준법 배지 */}
        <div style={{ background: '#f2f4f6', borderRadius: 8, padding: '10px 14px', fontSize: 12, color: '#666', marginBottom: 20, lineHeight: 1.6 }}>
          준법감시인 심의필 2025-12047<br />(2025.12.02~2027.12.31)
        </div>

        <div style={{ marginBottom: 12 }}>
          <span className="tag tag-pink" style={{ marginBottom: 12, display: 'inline-block' }}>원금손실가능상품</span>
        </div>
        <div style={{ fontSize: 22, fontWeight: 800, color: '#111', lineHeight: 1.35, marginBottom: 20 }}>
          (비고난도) 공모형 집합투자증권<br />상품설명서
        </div>

        <div style={{ background: '#f8fafc', borderRadius: 10, padding: '14px', marginBottom: 20, fontSize: 13, color: '#555', lineHeight: 1.7 }}>
          ※ 본 서류는 관련법령 및 내부통제기준에 따른 절차를 거쳐 작성되었습니다.
        </div>

        <p style={{ fontSize: 14, color: '#333', lineHeight: 1.8, marginBottom: 20 }}>
          본 설명서는 고객님께서 가입하신 집합투자증권의 투자설명서, 간이투자설명서 외 판매사가 고객님께 안내해야하는 정보를 담고 있습니다. 따라서, 투자상품에 대한 정보가 필요하신 경우에는 교부 받으신 투자설명서, 간이투자설명서를 반드시 참고하시기 바랍니다. 본 상품은 일반 예금상품과 달리 <span style={{ color: '#dc2626', fontWeight: 600 }}>원금의 일부 또는 전부 손실이 발생할 수 있으며</span>, 투자로 인한 손실은 투자자 본인에게 귀속됩니다.
        </p>

        <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', marginBottom: 24 }}>
          <div style={{ background: '#dc2626', borderRadius: 6, padding: '4px 6px', fontSize: 10, fontWeight: 700, color: '#fff', flexShrink: 0, textAlign: 'center', lineHeight: 1.4 }}>
            예금보험공사<br />비보호
          </div>
          <p style={{ fontSize: 13, color: '#555', lineHeight: 1.6 }}>이 금융상품은 예금자보호법에 따라 보호되지 않습니다.</p>
        </div>

        {/* 주의사항 */}
        <div style={{ background: '#fff5f5', borderRadius: 12, padding: '16px', marginBottom: 24 }}>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 8 }}>
            <span style={{ color: '#dc2626', fontSize: 16 }}>⚠</span>
            <span style={{ fontWeight: 700, fontSize: 15, color: '#dc2626' }}>주의사항</span>
          </div>
          <p style={{ fontSize: 13, color: '#555', lineHeight: 1.7 }}>
            설명을 제대로 이해하지 못한 상태에서 설명을 이해했다는 서명을 하거나 녹취기록을 남길 경우 추후 권리구제가 어려울 수 있습니다.
          </p>
        </div>

        {/* 긴 본문 */}
        {[
          '[숙려제도 기간안내] 신규 신청일 다음 영업일로부터 2영업일간 숙려기간이 부여되며, 숙려기간 종료 후 1영업일간 청약의사확인*이 진행됩니다.',
          '[청약철회제도 대상자] 일반금융소비자 중에「모집기간이 있는 고난도 금융투자상품 가입자」에 한함(이 외 해당사항 없음) - 2021년 05월 10일부터 적용',
          '[청약철회제도 기간안내] 청약의사 확인일(숙려기간 종료 후 1영업일) 다음일 부터 7일간 영업점 방문하여 청약철회 신청서 작성 또는 인터넷뱅킹·스마트뱅킹을 통해 청약철회의 의사를 표시할 수 있습니다.',
          '[공통유의사항] 수령하신 설명서를 참고하시어 투자에 따르는 위험, 원금손실 가능성 등을 반드시 확인하시기 바랍니다.',
        ].map((text, i) => (
          <div key={i} style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
            <span style={{ color: '#aaa', flexShrink: 0 }}>•</span>
            <p style={{ fontSize: 13, color: '#555', lineHeight: 1.7 }}>{text}</p>
          </div>
        ))}
      </div>

      {/* 하단 */}
      <div style={{ padding: '12px 20px 24px', background: '#fff', flexShrink: 0 }}>
        {!scrolled && (
          <div style={{
            background: '#333', color: '#fff', borderRadius: 10,
            padding: '12px 16px', fontSize: 13, textAlign: 'center',
            marginBottom: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
          }}>
            ⚠ 내용을 끝까지 확인해 주세요.
          </div>
        )}
        <button className="btn-primary" onClick={onNext} disabled={!scrolled} style={!scrolled ? { background: '#c0cfe8' } : {}}>
          확인
        </button>
      </div>
    </div>
  );
}
