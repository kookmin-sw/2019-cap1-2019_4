#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

# Kookmin University
# School of Computer Science
# Capstone #4 Flex Ads
# 20163181 Hwang Soojin

# Python 의 AWS SDK 패키지인 boto3 를 import.
import boto3
from botocore.exceptions import ClientError
from os import environ

if __name__ == "__main__":

    # 삭제하고자 하는 collection id를 지정
    collectionId = 'flexads_face_collection_test'

    print('Attempting to delete collection ' + collectionId)
    # aws rekognition과 연동
    client = boto3.client('rekognition')

    statusCode = ''

    try:
        # rekognition의 delete_collection 명령으로 해당 id의 collection을 삭제함
        response = client.delete_collection(CollectionId = collectionId)

	# Status Code를 반환 후 출력하여 정상적으로 삭제됨을 알 수 있음
        statusCode = response['StatusCode']        
	print(collectionId + ' delete success!')

    except ClientError as e:
        # 존재하지 않는 collection을 삭제하려고 하였을 때
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print('The collection ' + collectionId + ' was not found')
        else:
            print('Error other than Not Found occured : ' + e.response['Error']['Message'])
        statusCode = e.response['ResponseMetadata']['HTTPStatusCode']

    # 해당 collection의 Status Code 를 반환함
    # 성공했을 경우 200, 존재하지 않는 collection의 삭제를 실행한 경우는 400을 반환함
    print('Operation returned Status Code : ' + str(statusCode))
    print('Done')
