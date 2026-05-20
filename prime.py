# v1. 초기 웹크롤링 스크립트 작성
# v2. Dynamic loading 대응을 위해 requests 대신 Selenium + BeautifulSoup 구조로 변경
# v3. headless 모드 및 크롬 드라이버 자동 설정(webdriver-manager) 추가
# v4. div.bbslist_ty_a 구조의 실제 HTML 레이아웃에 맞춰 soup.select 경로 수정 및 고도화

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def crawl_woori_recruit():
    url = "https://recruit.incruit.com/wooribank/job/"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(3) 
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # 실제 HTML 구조 반영: div.bbslist_ty_a 내부의 각 li 요소 추출
        job_listings = soup.select("div.bbslist_ty_a > ul > li") 
        
        print(f"=== 우리은행 채용 공고 수집 결과 (총 {len(job_listings)}건) ===")
        print("-" * 60)
        
        for idx, job in enumerate(job_listings, 1):
            link_tag = job.select_one("a")
            if link_tag:
                # strong 태그 안의 채용 제목 가져오기
                title_tag = link_tag.select_one("strong.title")
                title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
                
                # span.day em 태그 안의 접수 기간 가져오기
                date_tag = link_tag.select_one("span.day em")
                date_info = date_tag.get_text(strip=True) if date_tag else "기간 정보 없음"
                
                # 상대 경로 링크를 절대 경로로 보정
                link = link_tag.get('href', '')
                if link and not link.startswith("http"):
                    # '//'로 시작하는 경우와 그렇지 않은 경우 대응
                    if link.startswith("//"):
                        link = "https:" + link
                    else:
                        link = "https://recruit.incruit.com" + link
                    
                print(f"[{idx}] {title}")
                print(f"    기간: {date_info}")
                print(f"    링크: {link}")
                print("-" * 60)
                
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_woori_recruit()