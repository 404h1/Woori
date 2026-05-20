있다. 다만 먼저 **정확한 기대치 조정**이 필요해.

## 한 줄 결론
- **“개입하면 반드시 행동이 억제된다”**를 보장하는 연구는 거의 없음.
- 대신 경제학·심리학·행동과학에는  
  **경고, 마찰(friction), 냉각시간(cooling-off), 자기설명(self-explanation), 능동적 확인(active choice), 사회적 규범, 사전약속(pre-commitment), 인오큘레이션(inoculation)**  
  같은 개입이 **충동적·오판·사기 유발 행동을 유의미하게 줄인다**는 강한 근거가 많음.
- 특히 너희 아이디어에는
  1. **경고문만으로는 약하다**
  2. **능동적 응답/마찰/시간지연이 들어가야 효과가 커진다**
  3. **설명가능한 이유 제시 + 구체적 자기질문이 좋다**
  4. **고령층은 단순 경고보다 ‘행동 중단 + 제3자 확인’이 더 중요하다**
이 4개 메시지를 끌어오면 좋음.

아래는 **임팩트 있는 연구 15개+**를 주제별로 정리한 거야.  
대회용으로 쓰기 좋게 **“우리 아이디어에 주는 시사점”**까지 붙일게.

---

# A. 경고/알림만으로는 한계가 있고, “능동적 개입”이 더 효과적이라는 연구

---

## 1) Egelman, Cranor, Hong (2008)
### *You’ve Been Warned: An Empirical Study of the Effectiveness of Web Browser Phishing Warnings*
- 분야: 보안 경고, 행동실험
- 학회: CHI 2008
- 링크: https://dl.acm.org/doi/10.1145/1357054.1357247
- 임팩트: HCI/보안 경고 연구에서 매우 유명한 고전

### 핵심 내용
- 브라우저 피싱 경고를 어떻게 디자인하느냐에 따라 사용자의 무시율이 크게 달라짐
- 단순 경고문은 많이 무시됨
- **명확하고 행동 지향적인 경고**가 더 효과적

### 우리 아이디어 시사점
- “보이스피싱 의심됩니다” 같은 단순 팝업은 약함
- **왜 위험한지 + 무엇을 해야 하는지**까지 줘야 함
- 즉, XAI 설명과 구체 행동 유도가 필요

---

## 2) Akhawe & Felt (2013)
### *Alice in Warningland: A Large-Scale Field Study of Browser Security Warning Effectiveness*
- 분야: 현장실험
- 학회: USENIX Security 2013
- 링크: https://www.usenix.org/conference/usenixsecurity13/technical-sessions/presentation/akhawe
- 임팩트: 보안 경고 분야 대표 논문

### 핵심 내용
- 실제 대규모 사용자 데이터를 보면 많은 사용자가 경고를 습관적으로 무시
- 그러나 **인터럽션 강도(interruption strength)**와 **행동 단계 설계**가 중요

### 시사점
- 송금 직전 개입은 그냥 배너가 아니라  
  **플로우 자체를 끊는 강한 인터럽션**이어야 함
- 즉, “1회 경고”보다 “3분 냉각 + 음성 응답 + 상담 연결”이 더 근거 있음

---

## 3) Bravo-Lillo et al. (2013)
### *Your Attention Please: Designing Security-Decision UIs to Make Genuine Risks Harder to Ignore*
- 학회: SOUPS 2013
- 링크: https://www.usenix.org/conference/soups2013/proceedings/presentation/bravo-lillo
- 임팩트: 보안 의사결정 UI 연구에서 자주 인용

### 핵심 내용
- 경고를 사람들이 읽게 만드는 것 자체가 어렵다
- 하지만 **사용자가 반드시 처리해야 하는 구조**, 즉 능동적 결정 구조를 만들면 효과 개선

### 시사점
- 체크박스/확인 버튼보다
- **질문에 직접 답하게 하는 인터뷰형 구조**가 더 타당

---

## 4) Sunshine et al. (2009)
### *Crying Wolf: An Empirical Study of SSL Warning Effectiveness*
- 학회: USENIX Security 2009
- 링크: https://www.usenix.org/legacy/events/sec09/tech/full_papers/sunshine.pdf
- 임팩트: 보안 경고 고전

### 핵심 내용
- 경고가 너무 자주 뜨면 무시됨
- 높은 심각도 상황에서만 강한 경고를 써야 효과적

### 시사점
- 모든 송금에 인터뷰 걸면 안 됨
- **고위험 거래에만 정밀 개입**
- 이게 UX와 효과성을 동시에 확보

---

# B. “마찰(friction), 지연, 냉각시간”이 충동적/유해 행동을 줄인다는 연구

---

## 5) Thaler & Sunstein (2008)
### *Nudge*
- 책이지만 행동경제학에서 가장 영향력 큼
- 링크: https://yalebooks.yale.edu/book/9780300122237/nudge/
- 임팩트: 압도적

### 핵심 내용
- 사람은 완전합리적이지 않음
- 선택구조(choice architecture)를 바꾸면 행동을 바꿀 수 있음
- 작은 마찰, 기본옵션, 리마인더, 프레이밍이 큰 효과

### 시사점
- 송금 전 3분 지연, 위험 질문, 제3자 확인 버튼은 전형적 choice architecture 개입
- “사기 피해자도 스스로 송금한다”는 점에서 특히 유효

---

## 6) Kahneman (2011)
### *Thinking, Fast and Slow*
- 임팩트: 노벨상 연관, 매우 강력
- 핵심: 인간은 빠른 직관(System 1)과 느린 숙고(System 2)로 의사결정
- 사기 상황은 공포/긴급성으로 System 1을 과도하게 자극

### 시사점
- **시간지연과 질문은 System 2를 강제로 깨우는 장치**
- 너희의 “AI 인터뷰 + 냉각시간” 논리적 근거로 매우 좋음

---

## 7) Milkman, Minson, & Volpp (2014)
### *Holding the Hunger Games Hostage at the Gym: An Evaluation of Temptation Bundling*
- 분야: 자기통제, 행동개입
- 링크: https://pubsonline.informs.org/doi/10.1287/mnsc.2014.1901
- 임팩트: 행동경제학/실험경제학에서 널리 인용

### 핵심 내용
- 즉시 감정/욕구에 휘둘리는 행동은 환경 설계로 완화 가능

### 시사점
- 긴급·공포에 휩쓸린 송금 행동 역시  
  **즉각 실행을 지연시키는 구조**가 중요

---

## 8) Halpern et al. (2015)
### *Default options in advance directives influence how patients set goals for end-of-life care*
- 분야: 선택설계, 디폴트 효과
- PNAS
- 링크: https://www.pnas.org/doi/10.1073/pnas.1516301112
- 임팩트: 매우 높음

### 핵심 내용
- 디폴트와 선택구조가 실제 중요한 의사결정까지 바꿈

### 시사점
- 시니어 모드에서
  - 고위험 신규수취인 송금은 기본적으로 “보호절차 ON”
  - 보호자 알림 기본값 ON
이런 설계가 행동을 실질적으로 바꿀 수 있음

---

## 9) Johnson & Goldstein (2003)
### *Do Defaults Save Lives?*
- Science
- 링크: https://www.science.org/doi/10.1126/science.1091721
- 임팩트: 매우 높음, 디폴트 효과 대표작

### 핵심 내용
- 기본 옵션이 인간 행동을 극적으로 바꾼다

### 시사점
- 보이스피싱 고위험군의 보호모드 기본 활성화에 강한 근거
- “옵트인”보다 “보호 디폴트”가 효과적일 가능성

---

## 10) Madrian & Shea (2001)
### *The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior*
- QJE
- 링크: https://academic.oup.com/qje/article-abstract/116/4/1149/1937624
- 임팩트: 행동경제학 초고전

### 핵심 내용
- 사람은 생각보다 기본 옵션과 관성에 크게 좌우됨

### 시사점
- 시니어·취약계층용 보호 기능을 “원하면 켜는 옵션”으로 두면 이용률 낮음
- **기본 보호 모드**가 실제 채택률 높임

---

# C. 자기설명, 숙고 유도, 능동적 응답이 오판을 줄인다는 연구

---

## 11) Chi et al. (1989)
### *Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems*
- Cognitive Science
- 링크: https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1302_1
- 임팩트: 매우 높음

### 핵심 내용
- 자기설명(self-explanation)은 기계적 반응보다 더 깊은 인지처리를 유도
- 단순 확인보다 스스로 이유를 말하는 것이 판단 개선에 도움

### 시사점
- “계속하시겠습니까?”보다
- **“왜 이 송금을 하려고 하는지 직접 말하게 하는 것”**이 더 강한 개입
- 이건 너희의 음성 인터뷰에 아주 좋은 근거

---

## 12) Lerouge & Warlop (2006)
### *Why it is so hard to predict our partner's product preferences: The effect of target familiarity on prediction accuracy*
- 소비자 판단 연구
- 직접 사기 연구는 아니지만, 자동적 추정의 오류와 숙고 필요성 시사

### 시사점
- 사람은 자기 판단을 과신한다
- “나는 안 속아”가 아니라, 구조적 숙고 장치를 넣어야 함

---

## 13) Wilson & Schooler (1991)
### *Thinking Too Much: Introspection Can Reduce the Quality of Preferences and Decisions*
- JPSP
- 링크: https://psycnet.apa.org/record/1991-25734-001
- 임팩트 높음

### 핵심 내용
- 모든 자기성찰이 좋은 건 아님
- 잘못 설계된 질문은 오히려 판단을 흐릴 수 있음

### 시사점
- 인터뷰 질문은 길고 복잡하면 안 됨
- **짧고 구체적이며 사기 시나리오 중심**이어야 함
- 이건 질문 설계 시 매우 중요

---

## 14) Aronson, Fried, & Stone (1991)
### *Overcoming denial and increasing the intention to use condoms through the induction of hypocrisy*
- AJPH
- 링크: https://ajph.aphapublications.org/doi/pdf/10.2105/AJPH.81.12.1636
- 임팩트 높음

### 핵심 내용
- 사람은 자기 신념과 행동의 불일치를 인식하면 행동 수정 가능성이 커짐

### 시사점
- 예:
  - “공공기관은 안전계좌 이체를 요구하지 않습니다”
  - “그런데 지금 고객님은 안전계좌로 송금하려고 합니다”
- 이런 **인지부조화형 경고**는 단순 경고보다 강함

---

# D. 사기·기만·오정보에 대한 “인오큘레이션(inoculation)”과 사전 경고 연구

---

## 15) McGuire (1964)
### *Inducing resistance to persuasion*
- 고전 심리학
- 설득저항(inoculation theory)의 출발점
- 임팩트 매우 큼

### 핵심 내용
- 사람은 미리 약한 형태의 설득공격과 반박을 경험하면 실제 설득에 덜 당함

### 시사점
- “AI 보이스피싱 리허설”, “거래 전 교육형 개입”의 강한 이론 근거
- 시니어플러스 영업점 교육과 찰떡

---

## 16) van der Linden et al. (2017)
### *Inoculating the Public against Misinformation about Climate Change*
- Global Challenges
- 링크: https://onlinelibrary.wiley.com/doi/10.1002/gch2.201600008
- 임팩트 높음, 인오큘레이션 현대 응용 대표작

### 핵심 내용
- 간단한 사전 경고와 반박 프레임 제공이 허위정보 설득력을 낮춤

### 시사점
- 금융사기에서도
  - “검찰/금감원은 계좌이체를 요구하지 않습니다”
  - “안전계좌는 대표 사기표현입니다”
같은 사전 면역 메시지가 효과적일 수 있음

---

## 17) Roozenbeek & van der Linden (2019)
### *Fake news game confers psychological resistance against online misinformation*
- Palgrave Communications
- 링크: https://www.nature.com/articles/s41599-019-0279-9
- 임팩트 높음

### 핵심 내용
- 게임/체험형 사전 노출이 실제 속는 확률을 낮춤

### 시사점
- 01 문서의 **하마터면** 같은 시뮬레이션 교육,
- 혹은 너희가 제안할 수 있는 **개인화 보이스피싱 리허설**
에 매우 좋은 근거

---

## 18) Basol, Roozenbeek, & van der Linden (2020)
### *Good News about Bad News: Gamified Inoculation Boosts Confidence and Cognitive Immunity Against Fake News*
- Journal of Cognition
- 링크: https://journalofcognition.org/articles/10.5334/joc.91
- 임팩트 괜찮음

### 핵심 내용
- 게임화된 학습이 허위정보 식별력과 자신감을 높임

### 시사점
- 시니어 대상 교육형 PoC, 리허설형 개입 설계의 근거

---

# E. 사회적 규범·제3자 개입·책임 공유가 행동을 바꾼다는 연구

---

## 19) Cialdini, Reno, & Kallgren (1990)
### *A Focus Theory of Normative Conduct*
- JPSP
- 링크: https://psycnet.apa.org/record/1991-03184-001
- 임팩트 매우 높음

### 핵심 내용
- 사람은 사회적 규범이 두드러지면 행동을 바꿈

### 시사점
- “공공기관은 안전계좌 이체를 요구하지 않습니다”
- “대부분의 고객은 이런 경우 송금을 중단하고 상담을 선택합니다”
같은 **규범 기반 메시지**가 효과적일 수 있음

---

## 20) Schultz et al. (2007)
### *The constructive, destructive, and reconstructive power of social norms*
- Psychological Science
- 링크: https://journals.sagepub.com/doi/10.1111/j.1467-9280.2007.01917.x
- 임팩트 높음

### 핵심 내용
- 사회적 규범 메시지는 행동을 바꾸지만, 잘못 쓰면 역효과도 있음

### 시사점
- “많은 사람이 속습니다”보다
- “이 상황에서는 송금을 멈추고 확인하는 것이 일반적입니다”
같은 설계가 더 좋음

---

## 21) Goldstein, Cialdini, & Griskevicius (2008)
### *A Room with a Viewpoint: Using Social Norms to Motivate Environmental Conservation in Hotels*
- Journal of Consumer Research
- 링크: https://academic.oup.com/jcr/article/35/3/472/1795402
- 임팩트 높음

### 시사점
- 규범 메시지는 행동 전환에 실효가 있음
- “대부분의 고객은 이 상황에서 1332/은행 상담 후 송금을 진행합니다” 같은 문구의 근거

---

# F. 고령층, 사기 취약성, 감정·인지 저하 관련 연구

---

## 22) Denburg et al. (2007)
### *Poor decision making among older adults is related to elevated risk aversion and reduced learning from feedback*
- Neuropsychology
- 링크 탐색 가능
- 임팩트: 고령층 의사결정 연구에서 자주 인용

### 핵심 내용
- 일부 고령층은 피드백 학습과 위험 판단에 취약

### 시사점
- 시니어는 단순 경고보다
  **반복 확인, 느린 설명, 제3자 연결**이 필요

---

## 23) Lichtenberg, Stickney, & Paulson (2013)
### *Is Psychological Vulnerability Related to the Experience of Fraud in Older Adults?*
- Clinical Gerontologist
- 링크: https://www.tandfonline.com/doi/abs/10.1080/07317115.2012.749323
- 임팩트: 고령층 금융사기 연구에서 중요

### 핵심 내용
- 심리적 취약성, 고립감, 우울감, 낮은 웰빙이 사기 피해와 관련

### 시사점
- 시니어 보호는 단순 UI 문제가 아니라 **심리상태 개입**이 중요
- 너희의 “대화형 보호 게이트” 정당화 가능

---

## 24) Spreng et al. (2016)
### *Financial Exploitation Is Associated With Structural and Functional Brain Differences in Healthy Older Adults*
- Journals of Gerontology
- 링크 가능
- 임팩트: 고령층 금융착취 연구에서 꽤 알려짐

### 핵심 내용
- 건강한 고령자도 금융착취에 취약할 수 있음

### 시사점
- “정상 송금이니까 고객 책임”이 아니라
- **구조적 보호 설계 필요**의 근거

---

## 25) Boyle et al. (2012)
### *Poor decision making is a consequence of cognitive decline among older persons without Alzheimer’s disease or mild cognitive impairment*
- PLoS One
- 링크: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043697
- 임팩트 높음

### 핵심 내용
- 뚜렷한 질환이 없어도 인지 저하는 의사결정 저하와 연결

### 시사점
- 시니어용 추가 안전장치는 차별이 아니라 보호 장치라는 논리 가능

---

# G. 사기/피싱 직접 연구

---

## 26) Vishwanath et al. (2011 / 2018 계열 연구들)
### phishing susceptibility 관련 다수
- 예: *Why do people get phished? Testing individual differences in phishing vulnerability...*
- 인용수 높음
- 링크 예시: https://www.sciencedirect.com/science/article/abs/pii/S0747563211001458

### 핵심 내용
- 충동성, 습관적 클릭, 낮은 숙고, 낮은 보안 이해가 취약성에 영향

### 시사점
- 피싱은 단순 정보 부족보다 **행동 패턴** 문제
- 따라서 “거래 전 행동 개입”이 중요

---

## 27) Pattinson et al. (2012)
### *Why do some people manage phishing emails better than others?*
- Information Management & Computer Security
- 인용 꽤 있음

### 핵심 내용
- 사용자 특성에 따라 탐지 능력 차이 큼

### 시사점
- 시니어/취약계층 맞춤형 개입 정당화

---

## 28) Ferreira & Lenzini (2015)
### *An analysis of phishing in networks*
- 개별 논문보다 리뷰성 참고
- 피싱 방어는 기술+행동 결합이 핵심

### 시사점
- 순수 기술탐지보다 사용자 개입 설계 병행 필요

---

# H. 금융/소비자 보호 문맥에 바로 끌어오기 좋은 정책·행동경제학 근거

---

## 29) Benartzi et al. (2017)
### *Should Governments Invest More in Nudging?*
- Psychological Science
- 링크: https://journals.sagepub.com/doi/10.1177/0956797617702501
- 임팩트 높음

### 핵심 내용
- 넛지는 비용 대비 효과가 매우 높을 수 있음

### 시사점
- 은행 입장에서 “AI 인터뷰 + 지연 + 설명”은 고비용 시스템보다 저비용 고효율 소비자보호 넛지로 포장 가능

---

## 30) Sunstein (2017)
### *Behavioral Economics of Consumer Contracts*
- 소비자보호·규제 설계 관련
- 임팩트 있음

### 시사점
- 소비자보호는 정보제공만으로 부족하고,
- **선택구조 재설계**가 필요하다는 논리 강화

---

# 너희 아이디어에 가장 직접적으로 쓸 수 있는 “핵심 근거 8개”만 뽑으면

발표에는 전부 다 못 쓰니까, 아래 8개를 메인으로 추천해.

---

## 최우선 1
**Kahneman (2011), Thinking, Fast and Slow**
- 긴급·공포 상황은 빠른 직관이 지배
- **냉각시간과 질문은 숙고를 유도**

## 최우선 2
**Thaler & Sunstein (2008), Nudge**
- 작은 마찰과 선택설계로 행동 변화 가능
- **송금 직전 AI 게이트의 행동경제학적 정당화**

## 최우선 3
**Johnson & Goldstein (2003), Do Defaults Save Lives?**
- 디폴트는 행동을 크게 바꿈
- **시니어 보호모드 기본값 ON 설계 근거**

## 최우선 4
**Madrian & Shea (2001)**
- 사람은 관성과 기본옵션에 민감
- **보호기능 opt-in보다 default-on 추천**

## 최우선 5
**Egelman et al. (2008)**
- 단순 경고는 무시되지만, 설계에 따라 효과 차이 큼
- **경고 문구보다 행동지향형 인터럽션 필요**

## 최우선 6
**Akhawe & Felt (2013)**
- 현장 데이터에서 강한 인터럽션 중요
- **배너형 경고보다 흐름 중단형 개입 필요**

## 최우선 7
**Chi et al. (1989)**
- 자기설명은 깊은 사고 유도
- **“왜 송금하시는지 말해보세요”가 효과적**

## 최우선 8
**Lichtenberg et al. (2013) / Boyle et al. (2012)**
- 고령층 금융취약성은 실제 연구로 입증
- **시니어 전용 보호 절차 정당화**

---

# 발표용으로 바로 쓸 수 있는 문장

## 문장 1
> 행동경제학 연구에 따르면 사람은 긴급성과 공포에 노출되면 숙고보다 즉각 반응에 의존합니다(Kahneman, 2011). 따라서 보이스피싱 피해를 줄이려면 단순 경고보다 **행동을 잠시 멈추게 하는 마찰과 냉각시간**이 필요합니다.

## 문장 2
> 선택구조를 바꾸는 작은 개입만으로도 행동은 크게 달라질 수 있습니다(Thaler & Sunstein, 2008; Johnson & Goldstein, 2003). 저희는 이를 금융사기 예방에 적용해, **송금 직전 AI 인터뷰와 지연이체**를 설계했습니다.

## 문장 3
> 보안 경고 연구는 단순한 팝업이 자주 무시된다는 점을 보여줍니다(Egelman et al., 2008; Akhawe & Felt, 2013). 그래서 저희는 읽고 지나가는 경고가 아니라, **고객이 직접 말하고 답해야 하는 대화형 개입**을 제안합니다.

## 문장 4
> 자기설명(self-explanation)은 더 깊은 인지처리를 유도합니다(Chi et al., 1989). “계속하시겠습니까?”보다 “왜 이 송금을 하시는지 말씀해 주세요”가 더 강한 보호장치가 될 수 있습니다.

---

# 중요한 주의점
너희가 발표에서 **“이 개입은 반드시 피해를 막는다”**라고 말하면 위험해.  
심사위원이 바로 물 수 있음.

대신 이렇게 말해야 함:

> “행동경제학·심리학 연구에 따르면, 경고만 제시하는 방식보다  
> **마찰, 숙고 유도, 자기설명, 냉각시간, 보호 디폴트**가 위험한 행동을 유의미하게 감소시킬 가능성이 높습니다.  
> 저희는 이 근거를 금융사기 송금 맥락에 적용했습니다.”

이렇게 가야 안전하고 강함.

---

# 다음 단계로 내가 해줄 수 있는 것
원하면 바로 이어서 해줄게.

## 옵션 1
**이 30개 중에서 진짜 PPT에 넣을 10개만 골라서**
- 인용수/임팩트
- 핵심 도표 문장
- 발표용 한 줄
로 정리

## 옵션 2
**“AI 인터뷰 + 냉각시간 + 시니어 보호모드” 각각에 대응되는 근거표**
형식으로 정리

## 옵션 3
**보이스피싱/사기 맥락에 더 직접적인 논문만 추가로 15개 더**
찾아서 심화 정리

원하면 다음 답변에서  
**“대회 발표용 근거 논문 Top 12 표”**로 바로 정리해줄게.