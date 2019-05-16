# -*- coding: utf-8 -*-

# selenium 설치
# pip install selenium

# 브라우처 driver 설치 (현재 크롬 버전 확인 후 설치)
# - 크롬 드라이브 설치: https://sites.google.com/a/chromium.org/chromedriver/downloads

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import requests
import time

# Chorme driver가 설치되어 있는 path
path = './chromedriver'

# 광고 화면을 띄우는 창을 전체화면으로 설정
options = Options()
# options.add_argument('--start-fullscreen')
# 창 최대 크기 모드
options.add_argument('--start-maximized')

# TODO: 성재오빠 쪽에서 받아오기
user_id = "77"

# Chrome 창 띄우기
driver = webdriver.Chrome(path, chrome_options=options)
# 사용자의 아이디가 지정되어 있는 url로 접속
URL = 'https://~~~~.execute-api.us-west-2.amazonaws.com/show?user=' + user_id
response = requests.get(URL)

# 고객 아이디 / 이름,  추천 제품 아이디 / 이름 / 진열 구역,  광고 이미지 주소
uid = response.json()['user_id']
        # TODO: response.json()['user_name']
uname = "밍지수"
pname = response.json()['product_name']
paisle = response.json()['aisle']
url = response.json()['bucket_url']
# TODO: 성재오빠 쪽에서 받아오기
time = "2019-05-31 14:48:33:0000"

# 고객과 제품의 정보를 포함한 HTML 실행
driver.get('file:///C:/Users/blue8/OneDrive/Desktop/sns/index.html?user_id=' + str(uid) + '&user_name=' + uname + '&product_name=' + pname + '&bucket_url=' + url + '&product_aisle=' + str(paisle) + '&current_time=' + time)
