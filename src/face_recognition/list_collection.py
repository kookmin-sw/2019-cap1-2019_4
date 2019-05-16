#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

# Kookmin University
# School of Computer Science
# Capstone #4 Flex Ads
# 20163181 Hwang Soojin

# Python 의 AWS SDK 패키지인 boto3 를 import
import boto3

if __name__ == "__main__":

    # 반환할 collection의 ID 최대 수
    maxResults = 2

    # aws rekognition과 연동
    client = boto3.client('rekognition')

    print('Displaying collections')
    print('--------------------------------------------\n')
    # rekognition에 list_collections 명령으로 collection의 목록을 반환함
    response = client.list_collections(MaxResults = maxResults)

    # collection의 개수
    cnt = 0

    while True:
        collections = response['CollectionIds']

        # collection의 개수 파악
        for collection in collections:
            cnt = cnt + 1
            print(str(cnt) + '.\t' + collection)

        # NextToken 은 다음 결과 집합을 가져오는데 사용되는 토큰
        # response의 얼굴이 MaxResults의 값보다 많으면
        # list_collections 명령어로 다음 결과 집합을 가져옴
        if 'NextToken' in response:
            nextToken = response['NextToken']
            # rekognition에 list_collections 명령으로 NextToken의 collection 목록을 반환함
            response = client.list_collections(NextToken = nextToken, MaxResults = maxResults)
        else:
            break

    print('\n--------------------------------------------')
    print('Done')
