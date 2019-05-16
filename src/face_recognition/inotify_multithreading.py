# -*- coding: utf-8 -*-
# nstall 'inotify'
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
#
## Kookmin University
## School of Computer Science
## Capstone #4 Flex Ads
## 20132651 Lee Sungjae 

import inotify.adapters
import boto3
import time
import datetime
import threading

# Create S3, Rekognition and S3 Resource
# Create bucket name and collection id of rekognition
s3 = boto3.client('s3')
bucket_name = 'flexads-face-dataset'
s3res = boto3.resource('s3')
rekognition = boto3.client('rekognition', region_name = 'us-east-2')
collection_id = 'flexads_face_collection'

# Create inotify object

# monitor current directory with inotify object

filename_list = []
time_list = []

def detect_events(name):
  print('start ', name)
  i = inotify.adapters.Inotify()
  watch_path = './'
  i.add_watch(watch_path)
  for event in i.event_gen(yield_nones = False):
    (header, type_names, path, saved_filename) = event
    if type_names[0] == 'IN_CREATE':
      check = str(saved_filename)[9:15]

      filename_list.append(saved_filename)
      time_list.append(check)
#      print(saved_filename)

def rekog(name):
  print('start', name)
  while True:
    now = datetime.datetime.now()
    check_now = now.strftime("%H%M%S")
    if check_now in time_list:
      now_index = time_list.index(check_now)
      print('find!! ',filename_list[now_index])
      time.sleep(3)

if __name__ == "__main__":
  x = threading.Thread(target=detect_events, args=('thread 1', ))
  y = threading.Thread(target=rekog, args=('thread 2', ))
try:
  x.start()
  y.start()
except(KeyboardInterrupt, SystemExit):
  cleanup_stop_thread()
  sys.exit()




