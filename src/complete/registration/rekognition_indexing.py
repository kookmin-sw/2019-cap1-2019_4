# -*- coding: utf-8 -*-
## Kookmin University
## School of Computer Science
## Capstone #4 Flex Ads
## 20132651 Lee Sungjae

# add_member.py 는
# 추가하고자 하는 회원의 얼굴 데이터셋에 접근하여,
# local의 얼굴 이미지 데이터셋을 s3 로 전송하고,
# 입력받은 user_id 를 이용하여 rekognition 의 collection 에 학습시키는 코드입니다.

# local 의 이미지 데이터셋 리스트를 확인하기 위해 os 패키지를 사용합니다.
# aws 연결을 위해 boto3 패키지를 사용합니다.
# shell script 에서 실행하여, 파라미터를 입력하기 위해 sys 를 사용합니다.
import os
import boto3
import sys

# 학습을 위한 user_id 와 확인을 위한 user_name 을 arguments 에서 가져옵니다.
user_name = sys.argv[1]
user_id = sys.argv[2]

# 데이터셋의 위치를 path 에 저장하고, os.walk 를 이용해 root, directory, file 이름을 가져옵니다.
path = './' + user_name
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        files.append(os.path.join(r, file))

# s3 client 를 s3 로, s3 resource 를 s3res 로 생성합니다.
# 사용되는 bucket name 은 flexads-face-dataset 입니다.
s3 = boto3.client('s3')
s3res = boto3.resource('s3')
bucket_name = 'flexads-face-dataset'

# rekognition client 를 rekognition 으로 생성합니다.
# 사용되는 collection_id 는 flexads_face_collection_id 입니다.
rekognition = boto3.client('rekognition', region_name='us-east-2')
collection_id = 'flexads_face_collection_id'

# 2단계
# 한 이미지씩 접근하여 s3 업로드
for f in files:

    # DS Store 파일이 업로드 되지 않도록 처리합니다.
    if 'DS' in f:
        continue

    # directory 이름으로 작성된 얼굴의 주인 이름과, filename 을 분해합니다.
    # 해당 이름이 합쳐진 새로운 파일명을 생성합니다.
    img_class = user_id
    filename = f.split('/')[-1]
    filename_with_class = '_'.join([img_class, filename])
    print(filename_with_class)

    # 해당 파일을 s3 에 업로드합니다.
    s3.upload_file(f, bucket_name, filename_with_class)
    print(filename_with_class, ' upload done')

    # 3단계
    # 해당 이미지 학습
    # rekognition 의 index_faces 를 이용해 해당 이미지를 학습시킵니다.
    # ExternalImageId 가 해당 얼굴의 주인의 user_id(label)로 들어가야 합니다.
    response = rekognition.index_faces(CollectionId = collection_id,
    Image = {'S3Object':{'Bucket':bucket_name, 'Name':filename_with_class}},
    ExternalImageId = img_class,
    MaxFaces = 1,
    QualityFilter = 'AUTO',
    DetectionAttributes = ['ALL'])

    # 얼굴을 detect 한 결과를 반환받습니다.
    # 해당 이미지에 어느 좌표에 얼굴이 존재하는지 등이 출력됩니다.
    print('Results for'+ filename_with_class)
    for faceRecord in response['FaceRecords']:
        print('Face indexed :')
        print('     Face ID: ' + faceRecord['Face']['FaceId'])
        print('     Location: {}'.format(faceRecord['Face']['BoundingBox']))

    for unindexedFace in response['UnindexedFaces']:
        print('Face not indexed:')
        print('     Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print('     Reasons:')
        for reason in unindexedFace['Reasons']:
            print('     ' + reason)
    print()

    # 4단계
    # 해당 이미지를 S3 내의 trained 폴더로 이동
    # 분석이 완료된 이미지는 s3 의 trained 폴더로 이동합니다.
    # 기존의 이미지 파일은 삭제됩니다.
    new_filename = 'trained/' + img_class + '/' + filename_with_class
    s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s/%s'%(bucket_name, filename_with_class))
    s3res.Object(bucket_name, filename_with_class).delete()
