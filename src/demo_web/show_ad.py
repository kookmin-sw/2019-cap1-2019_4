# -*- coding: utf-8 -*-

# selenium 설치
# pip install selenium

# 브라우처 driver 설치
# - 크롬 드라이브 설치: https://sites.google.com/a/chromium.org/chromedriver/downloads

from selenium import webdriver
import re
import requests

# Chorme driver가 설치되어 있는 path
path = './chromedriver'

# 성재오빠 쪽에서 받아오기
user_id = "124"

# Chrome 창 띄우기
driver = webdriver.Chrome(path)
# 사용자의 아이디가 지정되어 있는 url로 접속
URL = 'https://xtvznzjl15.execute-api.us-west-2.amazonaws.com/show?user=' + user_id
response = requests.get(URL)

user_id = response.json()['user_id']
user_name = "밍지수"
product_id = response.json()['product_id']
product_name = response.json()['product_name']
bucket_url = response.json()['bucket_url']

driver.get('file:///C:/Users/blue8/OneDrive/Desktop/sns/myhomepage.html?user=' + str(user_id) + '&user_name=' + user_name + '&product_id=' + str(product_id) + '&product_name=' + product_name + '&bucket_url=' + bucket_url)
