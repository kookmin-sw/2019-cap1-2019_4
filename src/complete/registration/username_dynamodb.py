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

# 해당되는 변수를 이용하여 dynamodb 의 resource 를 생성하고, 접근한다.
# 이 때, region 은 oregon 인 us-west-2 로 설정한다.
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=dynamo_id,
    aws_secret_access_key=dynamo_key,
    region_name = 'us-west-2'
)

# dynamodb 의 Recommendation 테이블을 지정한다.
table = dynamodb.Table('Recommendation')

# 해당 테이블에 update_item 을 이용하여, user_id 로 접근한 다음
# user_name 을 입력받은 user_name 으로 변환한다.
response = table.update_item(
    Key={
        'user_id':user_id,
        'update_ver' : 1
    },
    UpdateExpression="set user_name = :u",
    ExpressionAttributeValues={
        ':u': user_name
    },
    ReturnValues="UPDATED_NEW"
)

# 정확하게 이름이 들어갔는지 확인하기 위해, get_item 을 이용하여 체크한다.
check_response = table.get_item(
    Key={
        'user_id' : user_id,
        'update_ver': 1
    }
)
check_username = check_response['Item']['user_name']
print('<<', check_username, '>> name has registered to <<', user_id, '>> user number.')
