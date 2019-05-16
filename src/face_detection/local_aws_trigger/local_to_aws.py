# -*- coding: utf-8 -*-
# To install 'inotify'
# $ pip install inotify --no-binary :all:
#
# To install 'boto3'
# $ pip install boto3
#
# To connect AWS, you should set up authentication credentials.
# note: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
#
#
# This is Amazon S3 Examples
# > https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html

import inotify.adapters
import boto3

# Create an S3 client
s3 = boto3.client('s3')

i = inotify.adapters.Inotify()

# monitor specific folders
# 기본 dir 에 python 파일이 존재하고, jetson 에 sd card 에서 detect 한 이미지가 업로드되는 상황
watch_path = '../../media/nvidia/test_sd'
i.add_watch(watch_path)

for event in i.event_gen(yield_nones = False):
    (header, type_names, path, saved_filename) = event
    # print("PATH=[{}]\tFILENAME=[{}]\tEVENT_TYPES={}".format(path, filename, type_names))

    # 모니터 하고 있는 폴더에 파일이 생성될 때만 실행
    if type_names[0] == 'IN_CREATE':

        # type_names[0]의 type은 유니코드인데
        # s3에 올리기 위해서는 string이어야 하기 때문에 "utf-8"로 인코딩
        upload_file_name = saved_filename.encode("utf-8")

        # *S3 업로드 설정*
        # s3에 올리고자 하는 파일의 이름(폴더에 저장된 파일의 이름)
        filename = upload_file_name

        # aws s3에서 저장을 원하는 bucket 지정
        bucket_name = 'flexadstest'

        # s3에서의 objectname 설정
        objectname = filename
        # objectname = 'FlexAds_logo_init.png'

        # upload the file to AWS S3
        # 업로드 할 파일의 이름을 지정할 때, 본 파일과 같은 경로에 저장할 수도 있기 떄문에
        # 파일 이름에 경로까지 지정해주어야 업로드가 정상적으로 작동함
        s3.upload_file(watch_path + filename, bucket_name, objectname)
