
Conversation with Gemini
보이스피싱 관련 뉴스를 수집하고



연도별로



인구통계학적 정보,



건수



범죄 유형



굳이굳이 거기 속아넘어간 포인트







에 대해 알고싶어



방법을 알려줘 

보이스피싱 뉴스에서 요구하신 5가지 핵심 요소(연도, 인구통계, 건수, 범죄 유형, 심리적 트리거)를 체계적으로 수집하고 분석하려면, 웹 크롤링 기술과 자연어 처리(LLM) 모델을 결합하는 방식이 가장 효율적입니다.

1
1단계: 텍스트 데이터 수집 (크롤링 및 플랫폼 활용)
뉴스 기사 원문 확보
빅카인즈(Big Kinds) 플랫폼을 활용하는 것을 추천합니다. 한국언론진흥재단에서 제공하며, '보이스피싱 피해', '사기 수법' 등의 키워드로 검색한 뒤 기사 메타데이터와 본문을 엑셀 형태로 한 번에 다운로드할 수 있습니다.

더 방대한 원문이 필요하다면 네이버 뉴스 API 와 파이썬(Python)의 BeautifulSoup 라이브러리를 사용해 특정 기간의 뉴스 본문을 직접 크롤링해야 합니다.

2
2단계: LLM을 활용한 정보 추출 프롬프트 설계
비정형 텍스트를 정형 데이터로 변환
수집한 줄글 형태의 뉴스 기사에서 원하는 변수만 정확히 뽑아내기 위해, 기사 본문을 LLM(Gemini, GPT 등) API에 통과시켜 JSON 형태로 결과를 반환하도록 자동화합니다. 추출 기준은 다음과 같이 설정합니다.

연도별 건수 : 기사 발행일 기준 연도를 추출하고, 기사 내에 언급된 '경찰청 집계', '피해 발생 건수' 등 거시적 통계 수치를 포착합니다.

인구통계학적 정보 : 개별 사건 기사에서 피해자의 연령대, 성별, 직업군(예: 20대 대학생, 60대 퇴직자)을 추출합니다.

범죄 유형 : 기관사칭형(검찰/금융감독원), 대출빙자형, 메신저피싱(가족/지인 사칭) 등으로 카테고리를 분류합니다.

속아넘어간 포인트 : '가짜 구속영장으로 인한 공포감', '자녀 납치 사진을 통한 패닉 유도', '저금리 대출 대환을 미끼로 한 절박함 악용' 등 피해자가 이성을 잃고 송금하게 된 결정적 계기(심리적 트리거)를 요약하도록 지시합니다.

3
3단계: 데이터 정제 및 DB 구축
분석을 위한 데이터프레임화
LLM을 통해 추출된 JSON 데이터를 파이썬의 Pandas 라이브러리를 활용해 표(데이터프레임) 형태로 변환합니다.

누락된 정보(예: 피해자 연령이 안 나온 기사)는 '결측치'로 처리하여 통계의 왜곡을 막습니다.

4
4단계: 교차 분석 및 인사이트 도출
연도별 트렌드와 심리적 취약점 매핑
시계열 분석 : 연도별로 어떤 범죄 유형 이 급증하고 감소했는지 추이를 확인합니다.

상관관계 분석 : 특정 인구통계학적 정보 와 자주 엮이는 범죄 유형을 매핑합니다.

정성적 패턴 분석 : 추출된 속아넘어간 포인트 들을 워드클라우드나 의미망 분석으로 시각화하여, 범죄자들이 가장 자주 찌르는 인간의 심리적 취약점(공포, 탐욕, 고립감 등)을 도출합니다.


위와 같은 파이프라인을 구축하면 대량의 뉴스 원문에서 질문하신 핵심 인사이트만 빠르고 정확하게 정제해낼 수 있습니다.

파이썬으로 데이터를 수집하는 기초 코드가 필요하신가요?

Yes

파이썬과 네이버 뉴스 API를 사용해 보이스피싱 기사를 수집하는 기본 코드를 작성해 줘.

네이버 뉴스 API를 사용하여 '보이스피싱' 관련 기사를 수집하고, 결과를 분석하기 좋게 Pandas 데이터프레임 으로 변환하는 파이썬 기본 코드입니다.

네이버 개발자 센터에서 발급받은 Client ID 와 Client Secret 을 코드에 입력한 후 사용하시면 됩니다.

Python
# v1. 네이버 뉴스 API를 활용한 보이스피싱 뉴스 수집 기본 코드 추가
import json
import urllib.request
import pandas as pd

def get_naver_news(search_keyword, client_id, client_secret, display_count=100, start_index=1):
    """
    네이버 뉴스 검색 API를 통해 기사를 수집하는 함수
    """
    encText = urllib.parse.quote(search_keyword)
    # 기사 수집 기준을 최신순(date) 대신 관련도순(sim)으로 하려면 정렬 옵션을 변경하세요.
    url = f"https://openapi.naver.com/v1/search/news.json?query={encText}&display={display_count}&start={start_index}&sort=date"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        
        if rescode == 200:
            response_body = response.read()
            return json.loads(response_body.decode('utf-8'))
        else:
            print(f"Error Code: {rescode}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def parse_news_results(news_data):
    """
    수집된 JSON 데이터에서 필요한 필드(제목, 링크, 요약본, 발행일)를 추출하여 데이터프레임으로 변환
    """
    if not news_data or 'items' not in news_data:
        return pd.DataFrame()
    
    news_list = []
    for item in news_data['items']:
        # HTML 태그 제거를 위한 간단한 정제
        title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
        description = item['description'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
        
        news_list.append({
            'Title': title,
            'Link': item['link'],
            'Description': description,
            'PubDate': item['pubDate']
        })
        
    return pd.DataFrame(news_list)

# --- 실행부 ---
if __name__ == "__main__":
    # 본인의 네이버 API 키를 입력하세요
    CLIENT_ID = "YOUR_NAVER_CLIENT_ID"
    CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"
    
    KEYWORD = "보이스피싱 피해"
    
    print(f"'{KEYWORD}' 검색어로 뉴스 수집을 시작합니다...")
    raw_data = get_naver_news(KEYWORD, CLIENT_ID, CLIENT_SECRET, display_count=100)
    
    df_news = parse_news_results(raw_data)
    
    if not df_news.empty:
        print(f"총 {len(df_news)}건의 뉴스 데이터를 성공적으로 수집했습니다.")
        # 데이터 수집 결과 확인
        print(df_news.head())
        
        # CSV 파일로 저장 (인코딩에 유의하세요)
        df_news.to_csv("voice_phishing_news.csv", index=False, encoding="utf-8-sig")
        print("voice_phishing_news.csv 파일로 저장이 완료되었습니다.")
    else:
        print("수집된 데이터가 없습니다. API 키나 쿼리를 확인하세요.")
코드 활용 및 고도화 팁
대량 데이터 수집 (Pagination)
네이버 API는 한 번의 요청에 최대 100개(display_count)의 결과만 반환합니다. 더 많은 과거 데이터를 수집하려면 start_index 값을 1, 101, 201처럼 100씩 증가 시키면서 루프를 돌려야 합니다. (최대 1,000개까지 조회 가능)

원문(Full Text) 크롤링
API가 제공하는 Description 은 본문의 일부를 요약한 텍스트입니다. 인구통계학적 정보나 '속아넘어간 구체적 포인트'를 정밀하게 추출하려면, 수집된 데이터프레임의 Link 주소(특히 네이버 뉴스 링크인 news.naver.com 형식)로 BeautifulSoup 나 Scrapy 를 이용해 본문 전체를 긁어오는 프로세스를 추가해야 효과적입니다.

날짜 데이터 정제
pubDate 는 수집 시 파싱하기 까다로운 문자열 포맷(Tue, 20 May 2026 14:00:00 +0900)으로 들어옵니다. 연도별 분석을 위해 pd.to_datetime() 을 활용하여 연도 데이터만 따로 파싱해 컬럼을 분리해 두는 것이 좋습니다.

수집된 텍스트에서 '속아넘어간 포인트'를 추출할 LLM 프롬프트 예시가 필요하신가요?

Yes

수집한 보이스피싱 뉴스 본문에서 범죄 유형, 피해자 정보, 심리적 트리거를 추출하기 위한 LLM 프롬프트 구조와 JSON 출력 형식을 설계해 줘.

프롬프트 엔지니어링 팩트 체크 결과, LLM에서 일관된 비정형 데이터를 추출하기 위해서는 '역할 부여', '명확한 변수 정의', 'JSON 스키마 강제' 세 가지 요소가 프롬프트에 명시적으로 포함되어야 합니다. 특히 인간의 인지적 취약점을 분석하기 위해 심리적 트리거 에 대한 정의를 인지 및 행동주의적 관점에서 구체화하여 설계했습니다.

아래는 파이썬 코드 내에서 사용할 수 있도록 구성된 프롬프트와 JSON 스키마 템플릿입니다.

Python
# v1. LLM 정보 추출용 프롬프트 및 JSON 스키마 템플릿 추가됨

# 1. 시스템 프롬프트 (System Prompt)
system_prompt = """
당신은 범죄 데이터 분석 및 정보 추출 전문가입니다. 
제공된 보이스피싱 뉴스 기사 본문을 읽고, 아래 정의된 추출 기준에 따라 정확하게 정보를 파싱하여 지정된 JSON 형식으로만 출력하십시오. 
기사 내용에 없는 정보는 절대로 유추하지 말고, 반드시 null 로 처리하십시오.

[추출 기준]
1. 범죄 유형 (crime_type): 기관사칭형, 대출빙자형, 메신저피싱(지인사칭), 기타 중 하나로 분류.
2. 인구통계학적 정보 (demographics):
   - age: 피해자의 연령대 (예: "20대", "60대 이상")
   - gender: 피해자의 성별 ("남성", "여성")
   - occupation: 피해자의 직업군 (예: "대학생", "자영업자", "퇴직자")
3. 발생 건수 (incident_count): 기사 내에 명시된 특정 사건의 피해 발생 건수 (정수형). 단일 사건인 경우 1.
4. 발생 연도 (incident_year): 범죄가 발생했거나 통계가 집계된 연도 (YYYY 형식).
5. 심리적 트리거 (psychological_trigger): 피해자가 이성적 판단을 잃고 송금/이체하게 된 결정적 원인. (예: "고압적 수사관 연기를 통한 공포감 조성", "저금리 대환 대출을 미끼로 한 경제적 절박함 악용", "자녀 납치 상황 연출로 인한 패닉 유도")
"""

# 2. 유저 프롬프트 (User Prompt)
user_prompt = f"""
아래 기사 본문에서 데이터를 추출하십시오.

[기사 본문]
{news_body_text}
"""

# 3. JSON 출력 스키마 (JSON Schema)
# OpenAI API, Gemini API 등의 'JSON Mode' 또는 'Structured Output' 활용 시 아래 구조를 전달합니다.
json_schema = {
    "type": "object",
    "properties": {
        "crime_type": {"type": "string"},
        "demographics": {
            "type": "object",
            "properties": {
                "age": {"type": "string", "nullable": True},
                "gender": {"type": "string", "nullable": True},
                "occupation": {"type": "string", "nullable": True}
            }
        },
        "incident_count": {"type": "integer", "nullable": True},
        "incident_year": {"type": "integer", "nullable": True},
        "psychological_trigger": {
            "type": "string", 
            "description": "행동을 유발한 결정적 기망 수단 및 피해자의 인지적 과부하 상태 요약"
        }
    },
    "required": ["crime_type", "demographics", "psychological_trigger"]
}
프롬프트 설계 핵심 포인트
심리적 트리거 의 구체화 : 단순한 사기 수법(예: '악성 앱 설치')을 추출하는 것을 넘어, 피해자의 인지적 과부하를 유도한 감정적, 상황적 맥락을 텍스트로 요약하도록 지시하여 데이터 분석의 질을 높였습니다.

엄격한 Null 처리 : 뉴스 기사는 수사 보안이나 개인정보 보호 등의 이유로 모든 정보를 담고 있지 않은 경우가 많습니다. 모델의 환각(Hallucination) 현상을 방지하기 위해, 본문에 없는 정보는 억지로 추론하지 말고 null 로 반환하도록 제약을 걸었습니다.

구조화된 객체 : 인구통계학적 정보 를 단일 문자열이 아닌 하위 딕셔너리 구조로 묶었습니다. 이렇게 설계하면 추후 추출된 JSON 목록을 Pandas의 json_normalize() 함수로 한 번에 평탄화(Flatten)하여 분석용 데이터프레임으로 만들기 매우 수월합니다.

프롬프트 추출 정확도가 떨어질 때 대처법이 궁금하신가요?

Yes

LLM의 정보 추출 정확도를 더 높이기 위해 시스템 프롬프트에 Few-Shot 예시를 어떻게 구성해서 넣어야 하는지 알려줘.

프롬프트 엔지니어링 팩트 체크 결과, 뉴스 기사처럼 형식이 자유롭고 누락된 정보가 많은 텍스트에서 일관된 JSON 데이터를 뽑아내려면 Few-Shot(소수 샷) 기법 이 필수적입니다. 특히 '심리적 트리거'와 같은 주관적 요약 지표의 경우, 예시를 주지 않으면 LLM이 제멋대로 문장을 길게 쓰거나 기사 전체를 복사하는 문제가 발생합니다.

Few-Shot 예시를 구성할 때는 다음 두 가지 원칙을 지켜야 합니다.

다양성 확보 : 모든 정보가 꽉 찬 완벽한 기사(Positive Case)와 정보가 상당수 누락된 기사(Edge Case)를 교차로 배치하여, 모델이 '모르면 Null로 처리한다'는 규칙을 학습하게 해야 합니다.

명확한 구분자 사용 : [Input] 과 [Output] 이라는 구조를 반복하여 입력과 출력의 매핑 관계를 강제해야 합니다.

아래는 기존 시스템 프롬프트에 Few-Shot 예시를 통합한 코드입니다.

Python
# v2. Few-Shot 예시가 추가됨, 기존 Zero-Shot 템플릿 일부가 삭제됨

system_prompt = """
당신은 범죄 데이터 분석 및 정보 추출 전문가입니다. 
제공된 보이스피싱 뉴스 기사 본문을 읽고, 아래 정의된 추출 기준에 따라 정확하게 정보를 파싱하여 지정된 JSON 형식으로만 출력하십시오. 
기사 내용에 없는 정보는 절대로 유추하지 말고, 반드시 null 로 처리하십시오.

[추출 기준]
1. 범죄 유형 (crime_type): 기관사칭형, 대출빙자형, 메신저피싱(지인사칭), 기타 중 하나.
2. 인구통계학적 정보 (demographics): age, gender, occupation.
3. 발생 건수 (incident_count): 정수형. (단일 사건은 1)
4. 발생 연도 (incident_year): 범죄 발생 연도 (YYYY).
5. 심리적 트리거 (psychological_trigger): 피해자가 송금하게 된 결정적 원인 요약.

[Few-Shot 예시]

## Example 1: 모든 정보가 포함된 완벽한 기사
Input:
"서울 서초경찰서는 15일, 검사를 사칭해 20대 취업준비생 B씨로부터 5000만원을 가로챈 보이스피싱 수거책을 구속했다고 밝혔다. 범인들은 B씨에게 '당신의 계좌가 대포통장 범죄에 연루되었다'며 가짜 구속영장을 카카오톡으로 보내 극도의 공포감을 조성한 뒤, 안전 계좌로 이체하라고 속인 것으로 드러났다."

Output:
{
    "crime_type": "기관사칭형",
    "demographics": {
        "age": "20대",
        "gender": null,
        "occupation": "취업준비생"
    },
    "incident_count": 1,
    "incident_year": 2026,
    "psychological_trigger": "대포통장 연루 및 가짜 구속영장 전송을 통한 극도의 공포감 조성"
}

## Example 2: 일부 정보가 누락된 기사 (Null 처리 학습)
Input:
"어제 오후, 저금리 대출을 미끼로 수백만 원을 뜯어낸 사기범이 검거되었다. 이들은 기존 대출금을 갚으면 더 낮은 이자로 대환대출을 해주겠다며 서민 피해자들에게 선입금을 요구했다."

Output:
{
    "crime_type": "대출빙자형",
    "demographics": {
        "age": null,
        "gender": null,
        "occupation": null
    },
    "incident_count": null,
    "incident_year": 2026,
    "psychological_trigger": "저금리 대환 대출을 미끼로 한 경제적 절박함 악용"
}
"""
Few-Shot 템플릿의 핵심 설계 의도
성별(gender) 결측 유도 : 첫 번째 예시에서 B씨라는 단서만으로는 성별을 확정할 수 없으므로 null 로 처리하는 모습을 직접 보여주어, LLM이 넘겨짚어 추론하는(Hallucination) 현상을 차단했습니다.

연도 보정 : 기사에 '15일'이나 '어제'로만 표기된 경우, 크롤링 당시의 메타데이터(발행 연도)를 바탕으로 2026 처럼 정확한 연도를 기입하도록 모델의 판단 기준을 세워줍니다.

추출된 다량의 JSON을 데이터프레임으로 묶는 코드가 필요하신가요?