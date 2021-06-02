
from selenium import webdriver

import time
from bs4 import BeautifulSoup
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["출발시간", "가격"])


# selenium을 사용해서 사이트 직접 열기
driver = webdriver.Chrome(executable_path='C:/user/크롤링/chromedriver.exe')
driver.maximize_window() # 윈도우 창 최대화

# url 로 이동
url = "https://flight.naver.com/flights/results/domestic?trip=OW&fareType=YC&scity1=KWJ&ecity1=CJU&adult=9&child=0&infant=0&sdate1=2021.07.11."
driver.get(url)



time.sleep(5)
# 스크롤 내리기 위한 파이썬 코드

driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

#테스트

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")



# 3. 컨테이너 선택 select함수 사용
#container = soup.select(
#    'div.trip_result.ng-scope > ul > li'
#    )

#각 컨테이너별 데이터 수집: select_one 함수 사용
#반복문 이용하여 각 컨테이너별로 데이터 수집

#for con in container:
#    departing = con.select('dl:nth-child(1) > dd.txt_time.ng-binding')
#    print(departing.text)
#    price = con.select_one('div.txt_total > span.txt_pay.ng-binding')
#    print(price.text)


#    print("7월7일 광주->서울", "/", departing, "/", price)


# 3. 컨테이너 선택 select함수 사용
container = soup.select("li.trip_result_item")

#각 컨테이너별 데이터 수집: select_one 함수 사용
#반복문 이용하여 각 컨테이너별로 데이터 수집

for con in container:
    departing = con.select_one("dd.txt_time").text.strip()
    price = con.select_one("span.txt_pay").text.strip()
    sheet.append([departing, price])

wb.save("편도7월11일.xlsx")





