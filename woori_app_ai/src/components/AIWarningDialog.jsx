import { useState, useEffect, useRef } from 'react';
import botImg from '../assets/bot.png';
import {
  ACCOUNT,
  getNextCardPayment,
  getMonthlyAutoPayTotal,
  getDSR,
  getOverspentCategories,
  getPrimaryGoalProgress,
} from '../data/account';

/**
 * AI 경고 다이얼로그 — 가입 직전, 사용자 자산/펀드 정보 기반으로 3개 경고를 채팅 형태로 던짐.
 * 각 경고마다 "네, 그래도 진행할게요" / "다시 생각해볼게요" 선택.
 * 하나라도 "다시 생각" 누르면 onCancel.
 * 3개 모두 confirm 하면 onConfirm.
 */
export default function AIWarningDialog({ fund, investAmount, onConfirm, onCancel }) {
  const scrollRef = useRef(null);
  const [stage, setStage]   = useState(0); // 0~5: 인사 / Q1 / A1 / Q2 / A2 / Q3 / A3 / done
  const [answers, setAnswers] = useState([]); // ['proceed' | 'rethink', ...]

  const adv = fund.customAdvice;
  const loan = ACCOUNT.loans[0];
  const freeCash = ACCOUNT.monthly.freeCash;
  const overFreeFund = investAmount > (adv.freeFund - adv.emergency);
  const concentrationPct = ((investAmount / freeCash) * 100).toFixed(0);

  const worstYear = fund.region === '글로벌' ? '2022년 미국 긴축기' : '2022년';
  const worstLoss = -34;
  const lossAmount = Math.round(investAmount * (1 + worstLoss / 100));

  const nextCard = getNextCardPayment();
  const autoPayTotal = getMonthlyAutoPayTotal();
  const dsrPct = (getDSR() * 100).toFixed(1);
  const overspent = getOverspentCategories();
  const goal = getPrimaryGoalProgress();
  const goalDelayMonths = goal ? Math.ceil((investAmount - lossAmount) / goal.monthlyContribution) : 0;

  const warnings = [
    {
      icon: '💧',
      title: '유동성 경고 — 다음 결제 일정',
      message: `이번 달 자동이체로 ${autoPayTotal.toLocaleString()}원이 빠져나가요 (월세·대출이자·보험·통신비·적금). ${nextCard ? `게다가 ${nextCard.date.slice(5).replace('-', '/')}에 신용카드 ${nextCard.amount.toLocaleString()}원 결제 예정이에요. ` : ''}지금 ${investAmount.toLocaleString()}원을 펀드에 묶으면 통장 잔액이 빠듯해질 수 있어요. 펀드는 환매까지 3영업일 + 3개월 미만 환매 시 수수료 70%예요.`,
      question: '자동이체·카드 결제 일정 다 빠진 뒤에도 여유가 있으세요?',
    },
    {
      icon: '📉',
      title: '변동성 시뮬레이션 — 재무 목표 영향',
      message: `최근 3개월 ${fund.return3m}이지만, ${worstYear}에는 ${worstLoss}% 손실 사례가 있어요. 같은 상황이 오면 ${investAmount.toLocaleString()}원이 ${lossAmount.toLocaleString()}원이 됩니다 (-${(investAmount - lossAmount).toLocaleString()}원). ${goal ? `이혜원님이 설정한 "${goal.title}" 목표(${goal.progressPct.toFixed(0)}% 달성, ${goal.deadline.slice(0, 7)} 마감)가 손실 시 약 ${goalDelayMonths}개월 더 늦춰져요.` : ''}`,
      question: '재무 목표 지연을 감수하고도 진행하시겠어요?',
    },
    {
      icon: '🎯',
      title: '집중도 경고 — 부채 + 충동지출 신호',
      message: `월 여유자금 ${freeCash.toLocaleString()}원 중 ${concentrationPct}%를 이 펀드 하나에 넣으시는 거예요. 현재 DSR ${dsrPct}% (월소득 대비 대출상환), 신용대출 ${loan.balance.toLocaleString()}원 상환 중이에요. ${overspent.length > 0 ? `또 이번 달 ${overspent.map(o => `${o.label} +${o.diffPct.toFixed(0)}%`).join(', ')} — 평균 대비 과소비 패턴이 보여요. 충동 결정 아닌지 한 번 더 확인하세요.` : ''}`,
      question: '그래도 이 펀드 하나에 집중해서 진행하시겠어요?',
    },
  ];

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [stage]);

  // 초기 진입 시 0.5초 후 첫 인사
  useEffect(() => {
    const t = setTimeout(() => setStage(1), 600);
    return () => clearTimeout(t);
  }, []);

  const handleAnswer = (idx, choice) => {
    const next = [...answers, choice];
    setAnswers(next);
    if (choice === 'rethink') {
      // 다시 생각 → 즉시 cancel
      setTimeout(onCancel, 400);
      return;
    }
    if (next.length === warnings.length) {
      // 모두 confirm → 0.6초 후 최종 진행
      setTimeout(onConfirm, 800);
    } else {
      // 다음 경고로 진행
      setTimeout(() => setStage(s => s + 2), 600);
    }
  };

  const currentWarningIdx = Math.floor((stage - 1) / 2);
  const isAnsweredStage = stage % 2 === 0 && stage > 0;

  return (
    <>
      {/* 배경 dim */}
      <div style={{
        position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.7)', zIndex: 500,
        animation: 'fadeIn 0.3s ease-out',
      }} onClick={(e) => e.stopPropagation()} />

      {/* 풀스크린 채팅 */}
      <div style={{
        position: 'absolute', inset: 0, background: '#f8fafc',
        zIndex: 501, display: 'flex', flexDirection: 'column',
        animation: 'slideUpFade 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
      }}>
        {/* 헤더 */}
        <div style={{
          padding: '16px 20px', background: '#fff',
          borderBottom: '1px solid #f0f2f5',
          display: 'flex', alignItems: 'center', gap: 12,
        }}>
          <div style={{ width: 36, height: 36, borderRadius: '50%', overflow: 'hidden', flexShrink: 0 }}>
            <img src={botImg} alt="bot" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 14, fontWeight: 700, color: '#111' }}>WON AI 뱅커 — 최종 확인</div>
            <div style={{ fontSize: 11, color: '#dc2626', fontWeight: 600 }}>● 가입 전 위험 안내 진행 중</div>
          </div>
        </div>

        {/* 메시지 영역 */}
        <div ref={scrollRef} style={{
          flex: 1, overflowY: 'auto', padding: '20px',
          display: 'flex', flexDirection: 'column', gap: 16,
        }}>
          {/* 인사 메시지 */}
          {stage >= 1 && (
            <BotMessage delay={0}>
              <div style={{ fontSize: 14, color: '#111', lineHeight: 1.6 }}>
                <strong>이혜원 고객님,</strong> 가입 전에 3가지만 확인할게요.<br />
                마이데이터로 분석한 결과, <strong style={{ color: '#dc2626' }}>주의해야 할 점</strong>이 있어요.
              </div>
            </BotMessage>
          )}

          {warnings.map((w, idx) => {
            const showWarning = stage >= 1 + idx * 2;
            const showAnswered = answers.length > idx;
            if (!showWarning) return null;

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                <BotMessage delay={idx === 0 ? 0.6 : 0}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                      <span style={{ fontSize: 18 }}>{w.icon}</span>
                      <span style={{ fontSize: 14, fontWeight: 700, color: '#dc2626' }}>경고 {idx + 1}. {w.title}</span>
                    </div>
                    <div style={{ fontSize: 13, color: '#333', lineHeight: 1.7, marginBottom: 12 }}>{w.message}</div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: '#111', lineHeight: 1.6 }}>{w.question}</div>
                  </div>
                </BotMessage>

                {/* 사용자 응답 */}
                {showAnswered && (
                  <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                    <div style={{
                      background: '#e8effd', color: '#111', padding: '12px 16px',
                      borderRadius: '20px 4px 20px 20px', fontSize: 14, fontWeight: 600,
                    }}>
                      {answers[idx] === 'proceed' ? '네, 그래도 진행할게요' : '다시 생각해볼게요'}
                    </div>
                  </div>
                )}

                {/* 응답 버튼 (아직 안 누른 경고만) */}
                {!showAnswered && (idx === currentWarningIdx) && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 4 }}>
                    <button
                      onClick={() => handleAnswer(idx, 'rethink')}
                      style={{
                        padding: '14px', background: '#fff', color: '#dc2626',
                        border: '1.5px solid #dc2626', borderRadius: 12,
                        fontSize: 14, fontWeight: 700, cursor: 'pointer',
                      }}
                    >
                      다시 생각해볼게요
                    </button>
                    <button
                      onClick={() => handleAnswer(idx, 'proceed')}
                      style={{
                        padding: '14px', background: '#f2f4f6', color: '#555',
                        border: 'none', borderRadius: 12,
                        fontSize: 14, fontWeight: 600, cursor: 'pointer',
                      }}
                    >
                      네, 그래도 진행할게요
                    </button>
                  </div>
                )}
              </div>
            );
          })}

          {/* 모두 confirm 완료 */}
          {answers.length === warnings.length && answers.every(a => a === 'proceed') && (
            <BotMessage delay={0}>
              <div style={{ fontSize: 14, color: '#111', lineHeight: 1.6 }}>
                ✅ 모든 위험을 확인하셨어요. 가입 절차로 이동할게요.
              </div>
            </BotMessage>
          )}
        </div>
      </div>
    </>
  );
}

function BotMessage({ children, delay = 0 }) {
  return (
    <div className="animate-chat-appear" style={{ display: 'flex', gap: 10, animationDelay: `${delay}s`, opacity: 0, animationFillMode: 'forwards' }}>
      <div style={{ width: 32, height: 32, borderRadius: '50%', overflow: 'hidden', flexShrink: 0 }}>
        <img src={botImg} alt="bot" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>
      <div style={{
        flex: 1, background: '#fff', padding: '14px 16px',
        borderRadius: '4px 16px 16px 16px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
      }}>
        {children}
      </div>
    </div>
  );
}
