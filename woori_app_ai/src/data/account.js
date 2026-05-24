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
