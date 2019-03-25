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
i.add_watch('/tmp')


for event in i.event_gen():
    if event is not None:
        # (header, type_names, watch_path, filename) = event
        # test print
        print("check")
        # 파일 이름 지정 (이름 - 따로 지정하는 방법은 더 공부해야함)
        filename = 'Testflexads.png'
        # 버켓 이름 지정(default: flexadstest)
        bucket_name = 'flexadstest'

        # upload the file to AWS S3
        s3.upload_file(filename, bucket_name, filename)
