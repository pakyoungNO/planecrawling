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
strt = input("출발지 입력하기:")
arv = input("도착지 입력하기:")
#가고싶은 날짜 입력
yr = int(input("년도 입력:"))
mh = int(input("월 입력:"))
dy = int(input("날짜 입력:"))



#날짜 입력한게 올바른지 확인
time1 = datetime(yr, mh, dy, 23, 59, 59)
time2 = datetime.now()

nowyear = int(time2.year)
nowmonth = int(time2.month)

subyear = int(yr-nowyear)
submonth = int(mh-nowmonth)

#달력 넘기는 횟수
#11개월을 넘어가면 취소시킴
number1 = subyear * 12 + submonth
if number1 > 11:
    print("11개월 이내로 설정해주세요.")

#성인 소아 유아 숫자 체크
adu = int(input("성인 숫자:"))
kid = int(input("소아 숫자:"))
baby = int(input("유아 숫자:"))

if (adu + kid + baby) > 9:
    print("9명 이내로 해주세요")

#웹드라이버로 웹페이지 접근하기
driver = webdriver.Chrome(executable_path='C:/user/크롤링/chromedriver.exe')
driver.maximize_window() # 윈도우 창 최대화
driver.get('https://flight.naver.com/flights/')

driver.find_element_by_link_text("편도").click()

#출발지 선택
driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/fieldset/div[1]/div/div[1]/a[2]').click()
driver.implicitly_wait(1)
driver.find_element_by_link_text(strt).click()

sleep(0.4)

#도착지 선택
driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/fieldset/div[1]/div/div[2]/a[2]').click()
driver.implicitly_wait(1)
driver.find_element_by_link_text(arv).click()

#출발 날짜 선택
if time1 > time2 :
    driver.find_element_by_link_text("가는날 선택").click()
    driver.implicitly_wait(1)

    num = 0;
    while num < number1:
        driver.find_element_by_class_name("calendar-btn-next-mon.sp_flight").click()
        num = num + 1
    driver.find_element_by_link_text(str(dy)).click()


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

driver.find_element_by_class_name("sp_flight.btn_search.ng-scope").click()





