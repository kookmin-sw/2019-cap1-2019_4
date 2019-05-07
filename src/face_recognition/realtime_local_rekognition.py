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
#
## Kookmin University
## School of Computer Science
## Capstone #4 Flex Ads
## 20132651 Lee Sungjae 

import inotify.adapters
import boto3
import time

# Create S3, Rekognition and S3 Resource
# Create bucket name and collection id of rekognition
s3 = boto3.client('s3')
bucket_name = 'flexads-face-dataset'
s3res = boto3.resource('s3')
rekognition = boto3.client('rekognition', region_name = 'us-east-2')
collection_id = 'flexads_face_collection'

# Create inotify object
i = inotify.adapters.Inotify()

# monitor current directory with inotify object
watch_path = './'
i.add_watch(watch_path)

for event in i.event_gen(yield_nones = False):
    (header, type_names, path, saved_filename) = event

    # when file 'IN_CREATE', run below codes
    if type_names[0] == 'IN_CREATE':

        # change filename encoding type
        upload_file_name = saved_filename.encode("utf-8")
	print(upload_file_name, ' detected!')

        # filename is local filename, objectname is s3 filename
        filename = upload_file_name
        objectname = filename

        # upload the file to AWS S3
	# sleep 1 sec, because file write is not complete
	time.sleep(1)
        s3.upload_file(watch_path + filename, bucket_name, objectname)
	print(objectname, 'upload complete!')

	# response from rekognition with s3 face image
	response = rekognition.search_faces_by_image(CollectionId = collection_id,
	Image = {'S3Object':{'Bucket':bucket_name, 'Name':objectname}},
	MaxFaces = 1,
	FaceMatchThreshold=50)	
	
	
	if len(response['FaceMatches']) == 0:
		
    		# If there's no match face, send face image file to unknown directory in s3
    		print("No matches found, sending to unknown")
    		new_filename = 'unknown/%s' % filename
    		s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s/%s' % (bucket_name, filename))
    		s3res.Object(bucket_name, filename).delete()
	else:
		# If face matched, send face image file to detected directory in s3
		# print External Image Id (user name or user id )
		print ("Face found")
   		user_name = response['FaceMatches'][0]['Face']['ExternalImageId']
    		new_filename = 'detected/%s/%s' % (user_name, filename)
    		s3res.Object(bucket_name, new_filename).copy_from(CopySource='%s/%s' % (bucket_name, filename))
    		s3res.Object(bucket_name, filename).delete()
    		print('Found face is', user_name)


	
