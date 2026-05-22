import { useState } from 'react';
import StatusBar from '../components/StatusBar';

export default function Page08_HappyCall({ onClose, onDone }) {
  const [answered, setAnswered] = useState(false);

  return (
    <div className="phone-frame">
      <StatusBar />
      <div className="app-header">
        <h1>해피콜</h1>
        {!answered && (
          <button onClick={onClose} style={{ position: 'absolute', right: 16, background: 'none', border: 'none', fontSize: 22, cursor: 'pointer', color: '#333' }}>✕</button>
        )}
      </div>

      <div className="scroll-content" style={{ padding: '28px 20px 100px' }}>
        {!answered ? (
          <>
            <div style={{ fontSize: 22, fontWeight: 800, color: '#111', marginBottom: 6, lineHeight: 1.4 }}>
              상품 가입 시 확인한 내용을<br />선택해 주세요{' '}
              <span style={{ fontSize: 16, color: '#aaa', fontWeight: 400 }}>⊙</span>
            </div>

            <div style={{ padding: '20px 0', borderBottom: '1px solid #f0f2f5' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid #f0f2f5' }}>
                <span style={{ fontSize: 14, color: '#888' }}>가입일</span>
                <span style={{ fontSize: 14, color: '#111', fontWeight: 600 }}>2026.05.21</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0' }}>
                <span style={{ fontSize: 14, color: '#888' }}>상품명</span>
                <span style={{ fontSize: 13, color: '#111', fontWeight: 600, textAlign: 'right' }}>우리삼성그룹증권자투자신탁1호[주식]A-e</span>
              </div>
            </div>

            <div style={{ marginTop: 28 }}>
              <p style={{ fontSize: 15, fontWeight: 600, color: '#111', lineHeight: 1.6, marginBottom: 20 }}>
                가입일자 2026.05.21에 이혜원고객님 명의로 위 상품을 가입한 사실이 맞습니까?
              </p>
              {['예', '아니요'].map(label => (
                <button
                  key={label}
                  onClick={() => label === '예' && setAnswered(true)}
                  style={{
                    width: '100%', background: '#f8fafc',
                    border: '1px solid #e5e7eb', borderRadius: 12,
                    padding: '16px', fontSize: 16, color: '#222',
                    cursor: 'pointer', marginBottom: 10,
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  }}
                >
                  {label} <span style={{ color: '#ccc' }}>✓</span>
                </button>
              ))}
            </div>
          </>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', paddingTop: 120 }}>
            <div style={{
              width: 72, height: 72, borderRadius: '50%', background: '#1b64da',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 36, color: '#fff', marginBottom: 24,
            }}>
              ✓
            </div>
            <div style={{ fontSize: 24, fontWeight: 800, color: '#111', marginBottom: 12 }}>해피콜을 등록했어요</div>
            <div style={{ fontSize: 14, color: '#888' }}>[확인]을 누르면 첫 화면으로 이동해요.</div>
          </div>
        )}
      </div>

      {answered && (
        <div style={{ padding: '12px 20px 24px', background: '#fff', flexShrink: 0 }}>
          <button className="btn-primary" onClick={onDone}>확인</button>
        </div>
      )}
    </div>
  );
}
