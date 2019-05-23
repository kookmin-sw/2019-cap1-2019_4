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

# TODO
user_id = "12345678"

# Chrome 창 띄우기
driver = webdriver.Chrome(path, chrome_options=options)

# detectnet-camera facenet 에서 Detect 에 실패한 경우 ( 앞에 사람이 없는 경우 )
    # 디폴트 html 실행
driver.get('file_path/default.html')

# 사용자의 아이디가 지정되어 있는 url로 접속
URL = 'https://amazonaws_url/show?user=' + user_id
response = requests.get(URL)

# 고객 아이디 / 이름,  추천 제품 아이디 / 이름 / 진열 구역,  광고 이미지 주소
uid = response.json()['user_id']
uname = response.json()['user_name']
pname = response.json()['product_name']
paisle = response.json()['aisle']
url = response.json()['bucket_url']
# TODO
time = "2019-05-21 12:34:56:0000"

# Detect 되고 Rekognition 에 등록되어 있는 경우 ( 회원인 경우 )
    # 고객과 제품의 정보를 포함한 HTML 실행
driver.get('file_path/index.html?user_id=' + str(uid) + '&user_name=' + uname + '&product_name=' + pname + '&bucket_url=' + url + '&product_aisle=' + str(paisle) + '&current_time=' + time)

# Detect 는 되었지만 Rekognition 에 등록되어 있지 않은 사람인 경우 ( 비회원인 경우 )
    # 회원 등록 유도 HTML 실행
driver.get('file_path/nonmember.html?current_time=' + time)
