// 이혜원 고객 마이데이터 예시 — Page03/Page06/AIWarningDialog에서 공유

export const ACCOUNT = {
  customer: {
    name: '이혜원',
    age: 28,
    investorLevel: '첫 투자자',
    creditScore: 820,
    creditGrade: '1등급',
  },

  accounts: [
    {
      type: '입출금',
      name: 'WON통장',
      bank: '우리은행',
      number: '1002-067-468859',
      balance: 1547320,
      availableBalance: 300001,
    },
    {
      type: '적금',
      name: '우리 365일적금',
      bank: '우리은행',
      number: '1200-012-345678',
      balance: 3200000,
      monthlyDeposit: 200000,
      maturityDate: '2026-12-01',
    },
  ],

  monthly: {
    income: 2650000,
    fixedExpenses: {
      rent: 700000,
      insurance: 150000,
      loanRepayment: 300000,
      phone: 55000,
    },
    variableExpenses: {
      food: 320000,
      transport: 85000,
      shopping: 180000,
      medical: 40000,
      entertainment: 120000,
    },
    savings: 200000,
    freeCash: 300000,
  },

  loans: [
    {
      type: '신용대출',
      bank: '우리은행',
      balance: 30000000,
      monthlyPayment: 300000,
      interestRate: '4.5%',
      endDate: '2028-05-01',
    },
  ],

  investments: [],

  // 카드 사용 현황
  cards: [
    {
      type: '신용카드',
      name: '우리카드 카드의정석 EVERY POINT',
      limit: 3000000,
      thisMonthUsed: 423500,
      nextPaymentDate: '2026-06-05',
      nextPaymentAmount: 423500,
    },
    {
      type: '체크카드',
      name: 'WON체크카드',
      thisMonthUsed: 187200,
    },
  ],

  // 자동이체 캘린더 (매월)
  autoPayments: [
    { day: 5,  desc: '신용대출 이자', amount: 300000, kind: '대출' },
    { day: 25, desc: '실손보험 (메리츠화재)', amount: 150000, kind: '보험' },
    { day: 25, desc: '365일 적금', amount: 200000, kind: '적금' },
    { day: 27, desc: '월세 (집주인)', amount: 700000, kind: '주거' },
    { day: 28, desc: '통신비 (SKT)', amount: 55000, kind: '생활' },
  ],

  // 재무 목표 (사용자 설정)
  financialGoals: [
    {
      title: '전세보증금 모으기',
      target: 50000000,
      current: 16000000,
      deadline: '2027-06-30',
      monthlyContribution: 200000,
    },
  ],

  // 카테고리별 6개월 평균 vs 이번 달
  spendingTrend: {
    food:          { avg: 280000, current: 320000 },
    transport:     { avg: 90000,  current: 85000  },
    shopping:      { avg: 122000, current: 180000 },
    medical:       { avg: 25000,  current: 40000  },
    entertainment: { avg: 105000, current: 120000 },
  },

  recentTransactions: [
    { date: '05.23', desc: '월급 (주식회사 우리데이터)', amount: +2650000 },
    { date: '05.22', desc: '신용대출 상환', amount: -300000 },
    { date: '05.21', desc: '월세', amount: -700000 },
    { date: '05.20', desc: '식비 (배달의민족)', amount: -32500 },
    { date: '05.19', desc: '쇼핑 (쿠팡)', amount: -45800 },
    { date: '05.18', desc: '교통 (T-money충전)', amount: -50000 },
  ],
};

export const getTotalBalance = () =>
  ACCOUNT.accounts.reduce((sum, a) => sum + a.balance, 0);

export const getAvailableBalance = () =>
  ACCOUNT.accounts.find(a => a.type === '입출금')?.availableBalance ?? 0;

export const getMonthlyFreeCash = () => ACCOUNT.monthly.freeCash;

export const hasExistingInvestments = () => ACCOUNT.investments.length > 0;

export const getTotalLoanBalance = () =>
  ACCOUNT.loans.reduce((sum, l) => sum + l.balance, 0);

// DSR (월 부채상환액 / 월 소득) — 0~1
export const getDSR = () => {
  const monthlyDebt = ACCOUNT.loans.reduce((s, l) => s + l.monthlyPayment, 0);
  return monthlyDebt / ACCOUNT.monthly.income;
};

// 다음 카드 결제 정보
export const getNextCardPayment = () => {
  const credit = ACCOUNT.cards.find(c => c.type === '신용카드');
  return credit
    ? { date: credit.nextPaymentDate, amount: credit.nextPaymentAmount, name: credit.name }
    : null;
};

// 이번 달 자동이체 총액
export const getMonthlyAutoPayTotal = () =>
  ACCOUNT.autoPayments.reduce((s, p) => s + p.amount, 0);

// 평균 대비 +20% 초과 카테고리 (충동성 지출 감지)
export const getOverspentCategories = () => {
  const labels = { food: '식비', transport: '교통', shopping: '쇼핑', medical: '의료', entertainment: '여가' };
  return Object.entries(ACCOUNT.spendingTrend)
    .map(([k, v]) => ({
      key: k,
      label: labels[k] || k,
      avg: v.avg,
      current: v.current,
      diffPct: ((v.current - v.avg) / v.avg) * 100,
    }))
    .filter(c => c.diffPct >= 20);
};

// 재무 목표 진행률 (첫 번째 목표)
export const getPrimaryGoalProgress = () => {
  const g = ACCOUNT.financialGoals[0];
  if (!g) return null;
  return {
    ...g,
    progressPct: (g.current / g.target) * 100,
    remaining: g.target - g.current,
    monthsRemaining: Math.max(0, Math.round(
      (new Date(g.deadline) - new Date('2026-05-24')) / (1000 * 60 * 60 * 24 * 30)
    )),
  };
};
