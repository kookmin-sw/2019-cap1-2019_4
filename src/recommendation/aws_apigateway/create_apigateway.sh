#!/bin/bash

aws apigateway create-rest-api  \
 --region us-west-2 \
 --name 'Show Ads API' \
 --description 'Show recommended Ads to user'
