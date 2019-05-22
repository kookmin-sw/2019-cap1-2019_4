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
cd $user_name

# program start
./detectnet-camera facenet

# after 60s, program kill

