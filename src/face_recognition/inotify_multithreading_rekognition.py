# -*- coding: utf-8 -*-
## Kookmin University
## School of Computer Science
## Capstone #4 Flex Ads
## 20132651 Lee Sungjae

import inotify.adapters
import boto3
import time
import datetime
import threading

s3 = boto3.client('s3')
s3res = boto3.resource('s3')
rekognition = boto3.client('rekognition', region_name = 'us-east-2')

bucket_name = 'flexads-face-dataset'
collection_id = 'flexads_face_collection'

filename_list = []
time_list = []


def detect_events(name):
    print('Detect directory start! with ', name)
    i = inotify.adapters.Inotify()
    watch_path = './'
    i.add_watch(watch_path)

    for event in i.event_gen(yield_nones = False):
        (header, type_names, path, saved_filename) = event
        if type_name[0] == 'IN_CREATE':
            check = str(saved_filename)[9:15]
            filename_list.append(saved_filename)
            time_list.append(check)


def rekog(name):
    print('Recognition start! with ', name)
    while True:
        now = datetime.datetime.now()
        start = time.time()
        check_now = now.strftime("%H%M%S")
        if check_now in time_list:
            now_index = time_list.index(now_index)
            now_filename = filename_list[now_index]

            upload_filename = now_filename.encode("utf-8")
            print('Uploading', upload_filename, '...')
            time.sleep(1)
            s3.upload_file(watch_path + upload_filename, bucket_name, upload_filename)
            print('Uploading to s3 complete!')

            print('Get reponse from rekognition...')
            response = rekognition.search_faces_by_image(CollectionId = collection_id,
            Image = {'S3Object':{'Bucket':bucket_name, 'Name':upload_filename}},
            MaxFaces = 1,
            FaceMatchThreshold = 50)

            if len(reponse['FaceMatches']) == 0:
                print('No match face found, sending to unknown')
                new_filename = 'unknown/' + upload_file_name
                s3res.Object(bucket_name, new_filename).copy_from(CopySource=bucket_name + filename)
                s3res.Object(bucket_name, upload_filename).delete()
            else:
                print('Face found !!!')
        		user_name = response['FaceMatches'][0]['Face']['ExternalImageId']
        		new_filename = 'detected/%s/%s' % (user_name, filename)
        		s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s/%s' % (bucket_name, filename))
        		s3res.Object(bucket_name, filename).delete()
                print('------------------------------')
        		print('** Detected user is : ', user_name)
                print('------------------------------')

        end = time.time()
        print('Elapsed time : ', now - end)

if __name__ == "__main__":
    inotify_thread = threading.Thread(target = detect_events, args = ('Thread 1', ))
    rekognition_thread = threading.Thread(target = rekog, args = ('Thread 2', ))

    inotify_thread.start()
    rekognition_thread.start()
