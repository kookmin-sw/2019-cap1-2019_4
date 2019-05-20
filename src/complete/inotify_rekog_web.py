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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

driver_path = './chromedriver'
options = Options()
driver = webdriver.Chrome(driver_path, chrome_options = options)

base_url = 'your_aws_link'
base_html = 'file::///home/nvidia/my_web_location/index.html?'

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
        check_now = now.strftime("%H%M%S")
        if check_now in time_list:
	    start = time.time()
            now_index = time_list.index(check_now)
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

            if len(response['FaceMatches']) == 0:
                print('No match face found, sending to unknown')
                new_filename = 'unknown/' + upload_file_name
                s3res.Object(bucket_name, new_filename).copy_from(CopySource=bucket_name + filename)
                s3res.Object(bucket_name, upload_filename).delete()
            else:
                print('Face found !!!')
       		user_id = response['FaceMatches'][0]['Face']['ExternalImageId']
        	new_filename = 'detected/%s/%s' % (user_id, upload_filename)
       		s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s/%s' % (bucket_name, upload_filename))
        	s3res.Object(bucket_name, upload_filename).delete()
                print('------------------------------')
        	print('** Detected user_id is : ', user_id)
               	print('------------------------------')
	        print('Elapsed time : ', time.time() - start)
		
		info_response = requests.get(base_url + str(user_id))
		print(info_response.json())
		
		user_name = info_response.json()['user_name']
		product_name = info_response.json()['product_name']
		product_aisle = info_response.json()['aisle']
		image_url = info_response.json()['bucket_url']
		print(str(user_id), product_name, product_aisle, image_url) 
		driver.get(base_html + 'user_id=%s&user_name=%s&product_name=%s&bucket_url=%s&product_aisle=%s&current_time=%s'%(user_id, user_name, product_name, image_url, product_aisle, str(now)))

if __name__ == "__main__":
    inotify_thread = threading.Thread(target = detect_events, args = ('Thread 1', ))
    rekognition_thread = threading.Thread(target = rekog, args = ('Thread 2', ))

    inotify_thread.start()
    rekognition_thread.start()
