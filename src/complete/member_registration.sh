#!/bin/sh
echo -----------------------------------
echo Flex Ads Member Registration System
echo -----------------------------------
echo
# get user name and user id
echo Enter user-name for registration
read user_name
echo
echo Enter user-id for registration
read user_id
echo

# make user dataset directory
mkdir $user_name
echo \' $user_name \' directory created!
ls

#copy detectnet to user dataset directory
cp ./detectnet-camera $user_name

# change directory and run face detection
# with timeout 30s, detect and save face image in 30s
cd $user_name
timeout 30s ./detectnet-camera facenet

# remove detectnet-camera program from user dataset directory
rm ./detectnet-camera

# add user_name to DynamoDB with user_id
cd ../
python3 username_dynamodb.py $user_name $user_id

# face indexing to rekognition with user face dataset
python3 rekognition_indexing.py $user_name

echo
echo ++++++++++++++++++++++++++++++++++++
echo $user_name with $user_id Registered!
echo ++++++++++++++++++++++++++++++++++++
echo
