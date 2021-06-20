import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from time import sleep
from bs4 import BeautifulSoup
import openpyxl
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta






#엑셀 파일로 변경하기 위한 밑작업
"""
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["출발시간", "가격"])
"""
#값들 입력받기 (편도)
#출발지 도착지
sel_one_two = input("편도인지 왕복인지 적으시오:")

strt = input("출발지 입력하기:")
arv = input("도착지 입력하기:")
#가고싶은 날짜 입력
yr = int(input("출발년도 입력:"))
mh = int(input("출발월 입력:"))
dy = int(input("출발날짜 시작부분 입력:"))
dy_2 = int(input("출발날짜 끝부분 입력:"))
if sel_one_two == "왕복":
    howlong = int(input("기간을 입력:(며칠로 입력)"))
#성인 소아 유아 숫자 체크
adu = int(input("성인 숫자:"))
kid = int(input("소아 숫자:"))
baby = int(input("유아 숫자:"))

time2 = datetime.now()

nowyear = int(time2.year)
nowmonth = int(time2.month)

if (adu + kid + baby) > 9:
    print("9명 이내로 해주세요")

#웹드라이버로 웹페이지 접근하기
driver = webdriver.Chrome(executable_path='C:/user/크롤링/chromedriver.exe')
driver.maximize_window() # 윈도우 창 최대화
driver.get('https://flight.naver.com/flights/')



#출발지 선택
driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/fieldset/div[1]/div/div[1]/a[2]').click()
driver.implicitly_wait(1)
driver.find_element_by_link_text(strt).click()

sleep(0.4)

#도착지 선택
driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/fieldset/div[1]/div/div[2]/a[2]').click()
driver.implicitly_wait(1)
driver.find_element_by_link_text(arv).click()


# 성인 소아 유아 인원수 맞추기
driver.find_element_by_link_text("성인 1명").click()
driver.implicitly_wait(1)
lis = driver.find_elements_by_class_name("sp_flight.btn_increase")

a = int(1)
b = int(0)
c = int(0)

while a < adu:
    lis[0].click()
    a = a + 1
while b < kid:
    lis[1].click()
    b = b + 1
while c < baby:
    lis[2].click()
    c = c + 1

if kid > 0 and baby > 0:
    allakb = adu + kid + baby
    forwhat = "승객 {}명".format(str(allakb))
elif kid > 0:
    forwhat = "성인 {}명, 소아 {}명".format(str(adu), str(kid))
elif baby > 0:
    forwhat = "성인 {}명, 유아 {}명".format(str(adu), str(baby))
else :
    forwhat = "성인 {}명".format(str(adu))


driver.find_element_by_link_text(forwhat).click()


#이 항공 탐색 하기 전에 날짜들에 대한 정보를 여기에 몰아넣고 for문으로 돌려볼 계획이다.

#날짜 입력한게 올바른지 확인
for i in range(dy, dy_2+1):
    print("hello")

#time은 각각 그날에 대한 년도 월 일 시간 분 초를 기반으로 datetime함수로 작성된다.
#yr 원하는 출발 년도 mh는 월 i 는 일
    time1 = datetime(yr, mh, i, 23, 59, 59)

    subyear = int(yr-nowyear)
    submonth = int(mh-nowmonth)

#그 반복문을 쓸 때 달력이 계속 많이 넘어감을 방지하기 위해서
    nowyear = yr
    nowmonth = mh
#subyear는 0아니면 1이고
#submonth는 만약 mh가 12면 지금 6이기때문에 6이고            mh가 1이면 1-6해서 -5이다.

    if sel_one_two == "왕복":
        time3 = (time1 + timedelta(days=howlong))
    #도착일
        endyr = int(time3.year)
        endmh = int(time3.month)
        enddy = int(time3.day)

#만약 도착년도와 출발년도가 다르다면, 이것또한 넘겨줘야한다. ex 12월 25일출발 1월5일도착 ----> 12+(-11)
        sub2year = int(endyr-yr)
        sub2month = int(endmh-mh)
        number2 = sub2year * 12 + sub2month


#달력 넘기는 횟수
#11개월을 넘어가면 취소시킴
    number1 = subyear * 12 + submonth
    if number1 > 11:
        print("11개월 이내로 설정해주세요.")

#출발 날짜 선택

    driver.find_element_by_class_name("btn_trip.btn_trip_departure.unset").click()
    driver.implicitly_wait(1)

    num = 0
    while num < number1:
        driver.find_element_by_class_name("calendar-btn-next-mon.sp_flight").click()
        num = num + 1
    driver.find_element_by_link_text(str(i)).click()

    #편도일 경우는 편도만 클릭하고 내비둔다.
    #왕복일 경우는 위 왕복은 손대지 않고 아래 오는날 선택에 값을 집어넣는다.
    if sel_one_two == "편도":
        driver.find_element_by_link_text("편도").click()
    else:
        num2 = 0
        while num2 < number2:
            driver.find_element_by_class_name("calendar-btn-next-mon.sp_flight").click()
            num2 = num2 + 1
        driver.find_element_by_link_text(str(enddy)).click()



    driver.find_element_by_class_name("sp_flight.btn_search.ng-scope").click()



# -----------------------------------------------------------------------------------
#여기부터는 다음 페이지로 넘어가서 처리하는 과정을 담는다.
# -----------------------------------------------------------------------------------

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(["년도", "월", "일", "출발시간", "가격"])



    sleep(10)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    container = soup.select("li.trip_result_item")

    for con in container:
        departing = con.select_one("dd.txt_time").text.strip()
        price = con.select_one("span.txt_pay").text.strip()
        sheet.append([yr, mh, i, departing, price])

    wb.save("편도{}년 {}월 {}일.xlsx".format(yr, mh, i))
