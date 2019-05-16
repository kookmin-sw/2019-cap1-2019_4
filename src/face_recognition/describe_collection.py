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

    # 목록을 보고자 하는 collection id를 지정
    collectionId = 'flexads_face_collection'
    print('Attempting to describe collection ' + collectionId)
    # aws rekognition과 연동
    client = boto3.client('rekognition')

    try:
        # rekognition에 describe_collection 명령으로 해당 id의 collection 의 정보를 출력함
        response = client.describe_collection(CollectionId = collectionId)
        # 해당 collection의 ARN, Face Count, Face Model Version,
        # 해당 collection이 생성된 시간의 Timestamp를 출력
        print('Collection Arn : '  + response['CollectionARN'])
        print('Face Count : ' + str(response['FaceCount']))
        print('Face Model Version : ' + response['FaceModelVersion'])
        print('Timestamp : ' + str(response['CreationTimestamp']))

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print('The collection ' + collectionId + ' was not found' )
        else:
            print('Error other than Not Found occured : ' + e.response['Error'][ 'Message'])

    print('Done')
