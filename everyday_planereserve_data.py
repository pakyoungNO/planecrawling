# -*- coding: utf-8 -*-
import os
import selenium
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
import pandas as pd
import numpy as np
import glob
import sys




# driver로 flight 웹사이트에 접근
# 초기 값들 설정 (편도) + 도착지 리스트화시키기

arrli = ["제주", "김해/부산", "울산", "광주", "여수", "대구", "양양", "김포", "다낭", "방콕", "홍콩", "타이베이", "호치민시", "마닐라", "세부",	"하노이", "싱가포르", "코타키나발루", "나트랑", "쿠알라룸푸르", "오사카", "도쿄(나리타)",	"도쿄(하네다)", "후쿠오카",	"오키나와", "삿포로", "상하이", "청도", "광저우", "베이징", "연길", "심천", "LA", "하와이", "뉴욕(JFK)", "밴쿠버", "샌프란시스코", "토론토", "파리", "런던", "블라디보스토크", "로마", "프라하", "바르셀로나", "괌", "사이판", "시드니", "오클랜드", "브리즈번", "멜버른"]


#웹드라이버로 웹페이지 접근하기
driver = webdriver.Chrome(executable_path='C:/user/크롤링/chromedriver.exe')
driver.maximize_window() # 윈도우 창 최대화
driver.get('https://flight.naver.com/flights/')

driver.find_element_by_link_text("편도").click()


time2 = datetime.now()

nowyear = int(time2.year)
nowmonth = int(time2.month)
nowday = int(time2.day)

#출발지 선택--인천
driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/fieldset/div[1]/div/div[1]/a[2]').click()
driver.implicitly_wait(1)
driver.find_element_by_link_text("인천").click()

sleep(0.4)

# 도착 장소를 for문으로 받아주기
for i in arrli:
    print(i)
    # 도착지 선택
    driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/fieldset/div[1]/div/div[2]/a[2]').click()
    driver.implicitly_wait(1)
    driver.find_element_by_link_text(i).click()



    # 가는날 선택을 하루건너 하루로 만들어줘야함
    # 그리고 여기서 while문으로 검색해야함.

    # time3는 여기서 하루씩 이동할 년도를 의미함. 이 time3로 가는 날을 계속 바꾸어 줄것임.
    time3 = (time2 + timedelta(days=1))
    whatyear = int(time3.year)
    whatmonth = int(time3.month)
    whatday = int(time3.day)
    while whatyear == nowyear or whatmonth != nowmonth:
        try:
            driver.find_element_by_class_name("btn_trip.btn_trip_departure.unset").click()
            driver.implicitly_wait(1)


        #아래 if문은 달력을 한달 넘기기를 할지 말지 고민하는 문제이다.
            time1 = (time3 - timedelta(days=1))
            onedaybefore = int(time1.day)
            if whatday < onedaybefore:
                driver.find_element_by_class_name("calendar-btn-next-mon.sp_flight").click()


            driver.find_element_by_link_text(str(whatday)).click()

        # 항공권 검색을 누른다.
            driver.find_element_by_class_name("sp_flight.btn_search.ng-scope").click()

        # -----------------------------------------------------------------------------------
        # 여기부터는 다음 페이지로 넘어가서 처리하는 과정을 담는다.
        # -----------------------------------------------------------------------------------


            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(["외국", "현재년도", "월", "일", "찾는년도", "월", "일", "출발시간", "가격"])

            sleep(10)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            container = soup.select("li.trip_result_item")

            for con in container:
                departing = con.select_one("dd.txt_time").text.strip()
                price = con.select_one("span.txt_pay").text.strip()
                sheet.append([i, nowyear, nowmonth, nowday, whatyear, whatmonth, whatday, departing, price])

            wb.save("{}편도{}년_{}월_{}일작성_{}년{}월{}일출발.xlsx".format(i, nowyear, nowmonth, nowday, whatyear, whatmonth, whatday))

            time3 = (time3 + timedelta(days=1))
            whatyear = int(time3.year)
            whatmonth = int(time3.month)
            whatday = int(time3.day)
        except selenium.common.exceptions.ElementClickInterceptedException:
            time3 = (time3 + timedelta(days=1))
            whatyear = int(time3.year)
            whatmonth = int(time3.month)
            whatday = int(time3.day)
            pass
        except selenium.common.exceptions.NoSuchElementException:
            time3 = (time3 + timedelta(days=1))
            whatyear = int(time3.year)
            whatmonth = int(time3.month)
            whatday = int(time3.day)
            pass



