# -*- coding: utf-8 -*-

# selenium 설치
# pip install selenium

# 브라우처 driver 설치 (현재 크롬 버전 확인 후 설치)
# - 크롬 드라이브 설치: https://sites.google.com/a/chromium.org/chromedriver/downloads

from selenium import webdriver
import re
import requests

# Chorme driver가 설치되어 있는 path
path = './chromedriver'
# TODO: 성재오빠 쪽에서 받아오기
user_id = "23"

# Chrome 창 띄우기
driver = webdriver.Chrome(path)
# 사용자의 아이디가 지정되어 있는 url로 접속
URL = 'https://xtvznzjl15.execute-api.us-west-2.amazonaws.com/show?user=' + user_id
response = requests.get(URL)

# 고객 아이디 / 이름,  추천 제품 아이디 / 이름 / 진열 구역,  광고 이미지 주소
uid = response.json()['user_id']
            # TODO: response.json()['user_name']
uname = "밍지수"
            # TODO: 제품 아이디 필요한가?
pid = response.json()['product_id']
pname = response.json()['product_name']
# TODO: paisle = response.json()['product_aisle']
url = response.json()['bucket_url']

# 고객과 제품의 정보를 포함한 HTML 실행
# TODO: 새 창이 아닌 현재 창 띄우기 가능한지
# TODO: ('&product_aisle=' + str(paisle)) 추가, '&product_id=' + str(pid) 불필요시 제거
driver.get('file:///C:/Users/blue8/OneDrive/Desktop/sns/index.html?user_id=' + str(uid) + '&user_name=' + uname + '&product_id=' + str(pid) + '&product_name=' + pname + '&bucket_url=' + url)
