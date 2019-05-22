# -*- coding: utf-8 -*-
import boto3
import sys

# dynamo_credential 이라는 추가적인 python 파일을 생성하여
# dynamodb 접근 보안에 관련된 데이터를 분리하여 저장한다.
import dynamo_credential

# shell script 에서 전달받은 user_name 과 user_id 를 가져온다.
user_name = sys.argv[1]
user_id = sys.argv[2]

# 위에서 import 한 패키지에서 id 와 key 를 가져와 변수에 입력한다.
dynamo_id = dynamo_credential.key_id()
dynamo_key = dynamo_credential.access_key()

# 해당되는 변수를 이용하여 dynamodb 의 client 를 생성하고, 접근한다.
# 이 때, region 은 oregon 인 us-west-2 로 설정한다.
client = boto3.client(
    'dynamodb',
    aws_access_key_id=dynamo_id,
    aws_secret_access_key=dynamo_key,
    region_name = 'us-west-2'
)

# dynamodb 에 정상 접근되는지 테스트한다.
# 해당 코드는 dynamodb 에 user_id 로 접근하여, user_name 을 modify 하는 것으로 변경될 예정이다.
table_list = client.list_tables()['TableNames']
print(table_list)
