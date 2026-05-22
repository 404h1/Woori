import { useState } from 'react';
import './index.css';

import Page01 from './pages/Page01_InvestorInfo';
import Page02 from './pages/Page02_InvestmentResult';
import Page03 from './pages/Page03_FundList';
import Page03b from './pages/Page03b_FundDetail';
import Page04 from './pages/Page04_FundCompare';
import Page05 from './pages/Page05_InvestorCheck';
import Page06 from './pages/Page06_FundJoin';
import Page07 from './pages/Page07_Document';
import Page08 from './pages/Page08_HappyCall';

// 화면 순서
// 01(설문) → 02(결과) → 03(목록) → 03b(상세) 또는 04(비교) → 05(투자자확인) → 06(가입) → 07(설명서) → 08(해피콜)

export default function App() {
  const [page, setPage] = useState('01');

  const go = (p) => setPage(p);

  return (
    <>
      {page === '01' && <Page01 onNext={() => go('02')} />}
      {page === '02' && <Page02 onNext={() => go('03')} onBack={() => go('01')} />}
      {page === '03' && (
        <Page03
          onNext={() => go('04')}
          onFundDetail={() => go('03b')}
          onBack={() => go('02')}
        />
      )}
      {page === '03b' && (
        <Page03b
          onBack={() => go('03')}
          onJoin={() => go('05')}
        />
      )}
      {page === '04' && (
        <Page04
          onBack={() => go('03')}
          onJoin={() => go('05')}
        />
      )}
      {page === '05' && (
        <Page05
          onClose={() => go('06')}
        />
      )}
      {page === '06' && (
        <Page06
          onBack={() => go('05')}
          onNext={() => go('07')}
        />
      )}
      {page === '07' && (
        <Page07
          onClose={() => go('06')}
          onNext={() => go('08')}
        />
      )}
      {page === '08' && (
        <Page08
          onClose={() => go('06')}
          onDone={() => go('01')}
        />
      )}
    </>
  );
}

