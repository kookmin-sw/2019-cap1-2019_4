## Kookmin University
## School of Computer Science
## Capstone #4 Flex Ads
## 20132651 Lee Sungjae

# local_s3_face_search.py 는
# local 의 얼굴 이미지 1장을 s3 로 전송하고,
# 전송된 이미지를 rekognition 을 이용해 분석하여
# 해당 이미지가 어떤 학습된 인물을 의미하는지 출력하고,
# 학습이 완료된 이미지를 s3 에 정리하는 코드입니다.

# local 과 aws 의 연결을 위해 boto3 패키지를 사용합니다.
import boto3

# local 의 테스트 이미지인 'test_sungjae.jpeg' 파일을 지정합니다.
filename = 'test_sungjae.jpeg'

# s3 client 를 s3 로, s3 resource 를 s3res 로 생성합니다.
# 사용되는 bucket name 은 flexads-face-dataset 입니다.
s3 = boto3.client('s3')
s3res = boto3.resource('s3')
bucket_name = 'flexads-face-dataset'

# rekognition client 를 rekognition 으로 생성합니다.
# 사용되는 collection_id 는 flexads_face_collection 입니다.
# 이 때, s3 의 region 인 us-east-2 를 rekognition 에 명시하는 것이 중요합니다.
rekognition = boto3.client('rekognition', region_name = 'us-east-2')
collection_id = 'flexads_face_collection'

# 해당 이미지 파일을 s3 에 업로드합니다.
s3.upload_file(filename, bucket_name, filename)
print(filename, ' upload success')

# rekognition 의 search_faces_by_image 를 이용하여 해당 이미지의 얼굴 이름을 포함하여
# 응답 정보를 response 로 반환받아 저장합니다.
# 이 때, FaceMatchThreshold 를 70 으로 주었으며, 정확도를 조정할 수 있습니다.
response = rekognition.search_faces_by_image(CollectionId = collection_id,
Image = {'S3Object':{'Bucket':bucket_name, 'Name':filename}},
MaxFaces = 1,
FaceMatchThreshold=70)

# response 에 매치되는 얼굴 이미지의 개수에 따라 다르게 결과를 출력합니다.
# 만약 매치되는 얼굴이 없다면, 해당 이미지를 s3 의 unknown 으로 이동시킵니다.
if len(response['FaceMatches']) == 0:
    # no known faces detected, let the users decide in slack
    print("No matches found, sending to unknown")
    new_filename = 'unknown/%s' % filename
    s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s/%s' % (bucket_name, filename))
    s3res.Object(bucket_name, filename).delete()
# 매치되는 얼굴이 존재한다면, 해당 얼굴의 이름을 user_name 으로 저장하고, 출력합니다.
else:
    print ("Face found")
    print (response)
    # move image
    user_name = response['FaceMatches'][0]['Face']['ExternalImageId']
    new_filename = 'detected/%s/%s' % (user_name, filename)
    s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s/%s' % (bucket_name, filename))
    s3res.Object(bucket_name, filename).delete()
    print('Found face is', user_name)
