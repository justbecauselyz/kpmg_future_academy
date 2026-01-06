from bs4 import BeautifulSoup as BS
import urllib.request as req
import datetime
import os
import csv

# 2. html 가져오기
news_lists = []
def one_page_scraper(naver_url):
    html = req.urlopen(naver_url)

    # 3. HTML 파싱하기
    soup = BS(html, 'html.parser')

    # 4. 뉴스 목록(li태그) 추출하기 <- list
    # 반복되는 패턴을 찾아서 셀렉터로 지정
    lis = soup.select("ul.sa_list > li")
    news_lists = []
    for li in lis:
        title = li.select_one("strong.sa_text_strong").get_text().strip()
        press = li.select_one("div.sa_text_press").get_text().strip()
        image_url = li.select_one("img")

        if image_url:
            image_url = image_url.get("data-src") or image_url.get("src") or ""
            image_url = image_url.split("?")[0]
        else:
            image_url = 'img 없음'
        print(f"{title} - {press}\n Image Url : {image_url}")
        # 하나의 뉴스 정보를 전체목록 리스트에 추가
        news_lists.append([title, press, image_url])
    # print(news_list)

for num in range(100, 106):
    naver_url = f"https://news.naver.com/section/{num}"
    one_page_scraper(naver_url)

# 6. 리스트 -> 파일에 저장
# 현재 날짜/시간 가져오기
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d-%H")

# 폴더/파일명 설정
folder = "naver_news"
filename = f"{timestamp}.csv"
filepath = os.path.join(folder, filename)

# 폴더 자동 생성
os.makedirs(folder, exist_ok=True)

# CSV 파일로 저장
with open(filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Press", "Image URL"])
    writer.writerows(news_lists)
