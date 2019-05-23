# -*- coding: utf-8 -*-
## Kookmin University
## School of Computer Science
## Capstone #4 Flex Ads
## 20132651 Lee Sungjae

# dynamo_credential.py 코드는 AWS ID 와 KEY 를 외부에 저장하기 위한
# 간단한 모듈형 credential 코드입니다.
# import dynamo_credential 을 통해 패키지를 불러오고,
# dynamo_credential.key_id(), dynamo_credential.access_key() 를 통해서
# 이곳에 저장해 둔 ID 와 KEY 를 호출하는 것이 가능하다.

def key_id():
    return 'YOUR_AWS_ID'

def access_key():
    return 'YOUR_AWS_KEY'
