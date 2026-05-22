import StatusBar from '../components/StatusBar';

const FUND_A = {
  name: '삼성글로벌반도체증권자투자신탁H[주식]Ae',
  risk: '매우높은위험', riskClass: 'tag-red', region: '브릭스',
};
const FUND_B = {
  name: '우리삼성그룹증권자투자신탁1호[주식]A-e',
  risk: '높은위험', riskClass: 'tag-orange', region: '국내',
};

const ROWS = [
  { section: '기본정보', label: '상품개요',
    a: '반도체 관련 매출액 기준으로 전 세계 Top20 종목을 집중 투자하는 펀드',
    b: '삼성전자, 삼성물산, 삼성화재, 제일기획 등 각 업종별 경쟁력이 높은 삼성그룹주 중심의 포트폴리오 구성을 추구' },
  { label: '설정금액', a: '0', b: '0' },
  { label: '가입유형', a: '인터넷,스마트폰', b: '인터넷,스마트폰' },
  { label: '총보수', a: '연 1.26%', b: '연 0.86%' },
  { label: '선취수수료', a: '투자금액의 0.5%', b: '투자금액의 0.5%' },
  { label: '환매수수료', a: '', b: '' },
  { label: '기준가(전일대비)', a: '3,478.6', b: '2,935.97' },
  { section: 'TOP5 종목 정보', label: '종목1', a: 'SK하이닉스\n8.45%', b: '삼성전자\n28%' },
  { label: '종목2', a: 'MICRON TECHNOLOGY INC\n7.51%', b: '삼성전기\n12.43%' },
  { label: '종목3', a: 'APPLIED MATERIALS INC\n6.52', b: '삼성생명\n8.58%' },
  { label: '종목4', a: 'NVIDIA CORP\n6.05%', b: '삼성E&A\n7.65%' },
  { label: '종목5', a: 'LAM RESEARCH CORP\n4.98%', b: '삼성물산\n7%' },
  { section: '수익률 정보', label: '3개월', aRed: '+46.54%', bRed: '+38.82%' },
  { label: '12개월', aRed: '+153.30%', bRed: '+184.13%' },
];

export default function Page04_FundCompare({ onBack, onJoin }) {
  return (
    <div className="phone-frame">
      <StatusBar />
      <div className="app-header">
        <button className="back-btn" onClick={onBack} style={{ position: 'absolute', left: 4, zIndex: 100, padding: 12, cursor: 'pointer', background: 'transparent', border: 'none' }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>
        <h1>펀드 비교하기</h1>
      </div>

      <div className="scroll-content" style={{ paddingBottom: 100 }}>
        {/* 상단 펀드 헤더 */}
        <div style={{
          display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12,
          padding: '16px', borderBottom: '1px solid #f0f2f5',
        }}>
          {[FUND_A, FUND_B].map((fund, i) => (
            <div key={i} style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <span className={`tag ${fund.riskClass}`}>{fund.risk}</span>
              <div style={{ fontSize: 13, fontWeight: 700, color: '#111', lineHeight: 1.4 }}>{fund.name}</div>
              <div style={{ fontSize: 12, color: '#888' }}>| {fund.region}</div>
              <button
                onClick={onJoin}
                style={{
                  background: '#1b64da', color: '#fff', border: 'none',
                  borderRadius: 8, padding: '10px', fontSize: 13, fontWeight: 600, cursor: 'pointer',
                }}
              >
                가입하기
              </button>
            </div>
          ))}
        </div>

        {/* 비교 테이블 */}
        {ROWS.map((row, i) => (
          <div key={i}>
            {row.section && (
              <div style={{ padding: '12px 16px', background: '#f8fafc', fontWeight: 700, fontSize: 14, color: '#222', borderBottom: '1px solid #f0f2f5', borderTop: '1px solid #f0f2f5' }}>
                {row.section}
              </div>
            )}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', borderBottom: '1px solid #f0f2f5' }}>
              {[
                { val: row.aRed || row.a, isRed: !!row.aRed },
                { val: row.bRed || row.b, isRed: !!row.bRed },
              ].map((cell, ci) => (
                <div key={ci} style={{
                  padding: '14px 16px',
                  borderRight: ci === 0 ? '1px solid #f0f2f5' : 'none',
                }}>
                  {!row.section && i > 0 && (
                    <div style={{ fontSize: 12, color: '#aaa', marginBottom: 4 }}>{row.label}</div>
                  )}
                  {row.section && (
                    <div style={{ fontSize: 12, color: '#aaa', marginBottom: 4 }}>{row.label}</div>
                  )}
                  <div style={{
                    fontSize: 13, color: cell.isRed ? '#dc2626' : '#333',
                    fontWeight: cell.isRed ? 700 : 400,
                    lineHeight: 1.5, whiteSpace: 'pre-wrap',
                  }}>
                    {cell.val}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* 하단 고정 가입하기 */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        background: '#fff', borderTop: '1px solid #f0f2f5',
        padding: '12px 16px 24px',
      }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 10 }}>
          {[FUND_A, FUND_B].map((fund, i) => (
            <div key={i} style={{ fontSize: 11, color: '#333', fontWeight: 600, lineHeight: 1.4 }}>{fund.name}</div>
          ))}
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
          <button className="btn-primary" onClick={onJoin} style={{ padding: '12px', fontSize: 14 }}>가입하기</button>
          <button className="btn-primary" onClick={onJoin} style={{ padding: '12px', fontSize: 14 }}>가입하기</button>
        </div>
      </div>
    </div>
  );
}
