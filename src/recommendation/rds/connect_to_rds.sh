#! /bin/bash

# $1 : host
# $2 : user
# $3 : passwd
mysql --host=$1 --port=3306 --user=$2 --password=$3
