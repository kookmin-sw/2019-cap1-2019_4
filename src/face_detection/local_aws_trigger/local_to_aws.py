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
i.add_watch('./')

for event in i.event_gen(yield_nones = False):
    (header, type_names, path, saved_filename) = event
    # print("PATH=[{}]\tFILENAME=[{}]\tEVENT_TYPES={}".format(path, filename, type_names))

    # 모니터 하고 있는 폴더에 파일이 들어올 때만 실행
    if type_names[0] == 'IN_MOVED_TO':

        # type_names[0]의 type은 유니코드인데
        # s3에 올리기 위해서는 string이어야 하기 때문에 "utf-8"로 인코딩
        upload_file_name = saved_filename.encode("utf-8")


        # *S3 업로드 설정*
        # s3에 올리고자 하는 파일의 이름(폴더에 저장된 파일의 이름)
        filename = upload_file_name

        # aws s3에서 저장을 원하는 bucket 지정
        bucket_name = 'flexadstest'

        # s3에서의 objectname 설정
        # (폴더에 저장된 파일의 이름 그대로 s3에 저장하고 싶다면,
        # objectname = filename)
        objectname = 'FlexAds_logo_init.png'

        # upload the file to AWS S3
        s3.upload_file(filename, bucket_name, objectname)
