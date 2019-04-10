## Kookmin University
## School of Computer Science
## Capstone #4 Flex Ads
## 20132651 Lee Sungjae

## make_collection.py 는 Rekognition API 에 얼굴 정보를 학습시키기 위한
## 얼굴 모음 (collection) 을 생성하는 파이썬 코드이다.

## Python 의 AWS SDK 패키지 boto3 를 import 한다.
import boto3

if __name__ == "__main__":

    ## 특정 collection id 를 지정하여 해당 이름으로 생성한다.
    collectionId = 'flexads_face_collection'

    ## aws rekognition 과 연동한다.
    client = boto3.client('rekognition')

    print('Creating collection:' + collectionId)

    ## rekognition 에 create_collection 명령으로 해당 id 의 collection 을 생성한다.
    response = client.create_collection(CollectionId = collectionId)

    ## 해당 collection 의 ARN 과 Status Code 를 반환하여 출력한다.
    ## 이를 통해 정상적으로 생성되었는지 확인 가능하다.
    ## ARN 은 Amazon Resource Name 을 의미한다.
    print('Collection ARN : ' + response['CollectionArn'])
    print('Status code : ' + str(response['StatusCode']))
    print('Done')
