# -*- coding: utf-8 -*-
## Kookmin University
## School of Computer Science
## Capstone #4 Flex Ads
## 20132651 Lee Sungjae

# inotify_rekog_web.py 는 Flex Ads 시스템의 핵심 코드로
# inotify 와 AWS S3, Rekognition, API Gateway 호출, 그리고 웹 송출을 연동합니다.
# threading 을 활용하여 inotify 와 그 외의 기능을 thread 단에서 구분하였습니다.

# local file system 에 face image 생성을 탐지하기 위해 inotify 패키지를 가져옵니다.
# aws 연결을 위해 boto3 패키지를 가져옵니다.
# time 체크를 위해 time, datetime 패키지를 가져옵니다.
# multithreading 구현을 위해 threading 패키지를 가져옵니다.
# Image resize 를 통한 Network overhead 최소화를 위한 PIL 패키지를 가져옵니다.
import inotify.adapters
import boto3
import time
import datetime
import threading
from PIL import Image

# chrome 을 이용해 송출하기 위해 selenium 패키지를 가져옵니다.
# serverless 시스템에서 데이터를 가져오기 위해 requests 패키지를 사용합니다.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests


# 1. 기본 설정
# 1-1 chromedriver
# chromedriver 의 실행파일 위치와, 필요한 옵션을 설정하여 driver 객체를 생성합니다.
driver_path = './chromedriver'
options = Options()
driver = webdriver.Chrome(driver_path, chrome_options = options)

# 1-2 base serverless url and html location
# requests 를 통해 가져올 serverless 주소와
# chromedriver 를 통해 실행할 html 파일의 위치를 지정합니다

# base_url 은 회원 정보를 가져올 API Gateway 의 Serverless 주소입니다.
# default_html 은 아무도 인식되지 않았을 때, default 로 Flex Ads 로고를 보여줍니다.
# base_html 은 회원이 인식되었을 때, 전달하는 회원 정보를 기반으로 광고 정보를 보여줍니다.
# member_html 은 비회원이 인식되었을 때, 회원으로 등록해달라는 정보를 보여줍니다.
base_url = 'your_aws_link'
default_html = 'file:///home/nvidia/my_web_location/default.html'
base_html = 'file:///home/nvidia/my_web_location/index.html?'
member_html = 'file:///home/nvidia/my_web_location/nonmember.html'

# 1-3 aws client setting
# s3 와 rekognition client 를 생성합니다.
# 이 때, rekognition 의 region 을 s3 와 동일한 us-east-2 로 지정합니다.
# 추가적으로, bucket_name 과 collection_id 도 설정합니다.
s3 = boto3.client('s3')
s3res = boto3.resource('s3')
rekognition = boto3.client('rekognition', region_name = 'us-east-2')
bucket_name = 'flexads-face-dataset'
collection_id = 'flexads_face_collection_id'

# 1-4 global list variable for multithreading
# multithreading 에서 공유되는 전역변수 리스트 filename_list 와 time_list 를 명시합니다.
filename_list = []
time_list = []

# 2. detect_events with inotify
# inotify 를 이용하여 local 에 face image 가 생성되는 이벤트를 감지하는 코드입니다.
def detect_events(name):
    print('Detect directory start! with ', name)

    # 감지하고자 하는 watch_path 를 지정합니다.
    # 해당 path 를 inotify 객체에 add_watch 로 추가합니다.
    i = inotify.adapters.Inotify()
    watch_path = './'
    i.add_watch(watch_path)

    # event 가 생성될 때 마다, 해당 event 의 정보를 받아옵니다.
    for event in i.event_gen(yield_nones = False):
        (header, type_names, path, saved_filename) = event
        # detectnet-camera 에서 face image 를 생성하고, 완료되었을 때 IN_CLOSE_WRITE 조건이 나타납니다.
        # 해당 경우만 if 문을 사용하여 체크하고, filename_list 와 time_list 에 값을 저장합니다.
        if type_names[0] == 'IN_CLOSE_WRITE':
            check = str(saved_filename)[9:15]
            filename_list.append(saved_filename)
            time_list.append(check)

# 3. Recognize face, get member info from DynamoDB, show advertisement with selenium
def rekog(name):
    # rekog 함수가 시작되면, 기본 페이지로 이동하며
    # face image file 에 대한 miss, hit 을 확인하기 위한 miss_num 변수를 초기화합니다.
    print('Recognition start! with ', name)
    driver.get(default_html)
    miss_num = 0
    while True:
        # 3-1 time and filename check
        # multithreading 을 위해 먼저 현재 시간을 변수로 저장합니다.
	# 추가적으로, before_now 에 now 의 1초 전 시간을 변수로 저장합니다.
        now = datetime.datetime.now()
        before_now = now - datetime.timedelta(seconds=1)
	
	# 두 시간에 대한 HMS 정보를 check_now, check_before 에 저장합니다.
	# 1초 전의 file 까지 고려하여 시스템의 안정성을 높이기 위함입니다.
	check_now = now.strftime("%H%M%S")
	check_before = before_now.strftime("%H%M%S")
	
        # 두 시간중 하나라도 time_list 에 존재하면, 해당하는 filename 을 가져옵니다.
        if check_now in time_list or check_before in time_list:
	    if check_now not in time_list:
		check_now = check_before
	
	    # Latency 측정을 위한 start time 을 기록합니다.
	    start = time.time()
            now_index = time_list.index(check_now)
            list_filename = filename_list[now_index]
            
	    # 해당 filename 의 이미지를 resize_ratio 만큼 해상도를 낮추어 다시 저장합니다.
            change_filename = list_filename[:-4] + '_resize.PNG'
            resize_ratio = 0.8
            img = Image.open(list_filename)
            img_width, img_height = img.size
            print('Image size : ', str(img_width), str(img_height))
            
	    # Image.ANTIALIAS 옵션을 이용해 resize_size 만큼 이미지를 조정 및 저장합니다.
            resize_size = (img_width * resize_ratio, img_height * resize_ratio)
            img.thumbnail(resize_size, Image.ANTIALIAS)
            img.save(change_filename, "PNG")
            now_filename = change_filename
		
            # 3-2. Face image upload to S3
            # 해당 얼굴 이미지의 분석을 위해, 먼저 AWS S3 에 업로드 하는 과정이 필요합니다.
	    # IN_CLOSE_WRITE 는 이미지 파일의 Write 작업이 완료되었다는 의미이므로, 1초 기다려 줄 필요가 없습니다.
            upload_filename = now_filename.encode("utf-8")
            print('Uploading', upload_filename, '...')
            s3.upload_file(upload_filename, bucket_name, upload_filename)
            print('Uploading to s3 complete!')

            # 3-3. Face image recognition with AWS Rekognition
            # S3 에 업로드된 파일을 이용하여, rekognition 에 response 를 보낸다.
            # FaceMatchThreshold 는 기존의 50에서 조금 더 높여 80으로 설정한다.
            print('Get response from rekognition...')
            try:
                response = rekognition.search_faces_by_image(CollectionId = collection_id,
                Image = {'S3Object':{'Bucket':bucket_name, 'Name':upload_filename}},
                MaxFaces = 1,
                FaceMatchThreshold = 80)

                # 만약 매칭되는 얼굴이 없다면, 해당 사실을 알리고 파일을 unknown 으로 이동시킨다.
                if len(response['FaceMatches']) == 0:
                    print('No match face found, sending to unknown')
                    new_filename = 'unknown/%s'%(upload_filename)
                    s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s%s'%(bucket_name,upload_filename))
                    s3res.Object(bucket_name, upload_filename).delete()
			
		    # 매칭되는 얼굴이 없다는 것은, 회원이 아니라는 의미이므로 회원 등록 권유 페이지를 보여준다.
		    # 이 때, 현재 시간에 대한 변수도 함께 전달한다.
		    # 의미있는 화면 송출이 존재했기 때문에, miss_num 을 0으로 초기화 한다.
		    miss_num = 0
		    driver.get(member_html + 'current_time=%s'%(str(now)))
                # 매칭되는 얼굴이 있다면, 해당 얼굴의 user_id 를 반환하게 된다.
                else:
                    print('Face found !!!')
               	    user_id = response['FaceMatches'][0]['Face']['ExternalImageId']
                    new_filename = 'detected/%s/%s' % (user_id, upload_filename)
               	    s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s/%s' % (bucket_name, upload_filename))
                    s3res.Object(bucket_name, upload_filename).delete()

                    # 반환된 얼굴의 user_id 정보를 기반으로, serverless 를 통해 DynamoDB 에서 회원 정보를 가져온다..
            	    info_response = requests.get(base_url + str(user_id))

                    # 해당 정보에서 user_name, product_name, aisle, bucket_url 을 가져온다.
            	    user_name = info_response.json()['user_name']
            	    product_name = info_response.json()['product_name']
            	    product_aisle = info_response.json()['aisle']
            	    image_url = info_response.json()['bucket_url']

                    # Recognize 된 회원의 이름 정보를 출력한다.
                    print('--------------------------------')
            	    print('** Detected user_id is : ', user_name)
                    print('--------------------------------')
    	            print('Elapsed time : ', time.time() - start)

                    # chromedriver 측에 해당 정보를 전송하여 광고가 송출되도록 한다.
		    # 의미있는 정보가 전달되었기 때문에, miss_num 을 0으로 초기화한다.
		    miss_num = 0
            	    driver.get(base_html + 'user_id=%s&user_name=%s&product_name=%s&bucket_url=%s&product_aisle=%s&current_time=%s'%(user_id, user_name, product_name, image_url, product_aisle, str(now)))

	    # 사람이 아닌 이미지가 Rekognition 에 들어갔을 경우에, default 페이지를 보여다.
            except:
		print('non-face image detected in detectnet')
		driver.get(default_html)
		time.sleep(3)
		
	# 현재 시간에 적절한 filelist 가 존재하지 않을 경우, miss 라 한다.
	# 이 경우에는 default 페이지를 송출해야 하는데, 이전의 페이지에서 바로 변할 경우
	# 사용자 경험이 나쁘기 때문에 이를 위해 3회 연속 miss 가 발생할 경우 default 페이지를 송출한다.
	# 송출 후에는 miss counter 인 miss_num 을 0으로 초기화한다.
	# 1회 miss 발생은 2초의 Latency를 갖는다.
	else:
	    print('filelist - miss')
	    time.sleep(2)
	    miss_num = miss_num + 1
	    if miss_num == 3:
	        miss_num = 0
		driver.get(default_html)

if __name__ == "__main__":
    # 서로 다른 두 개의 Thread 를 객체로 생성한다.
    inotify_thread = threading.Thread(target = detect_events, args = ('Thread 1', ))
    rekognition_thread = threading.Thread(target = rekog, args = ('Thread 2', ))

    # 각각의 Thread 를 병렬적으로 실행한다.
    inotify_thread.start()
    time.sleep(1)
    rekognition_thread.start()
