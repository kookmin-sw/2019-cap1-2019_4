#!/bin/bash

aws dynamodb create-table \
    --table-name Recommendation \
    --attribute-definitions \
        AttributeName=user_id,AttributeType=N \
        AttributeName=update_ver,AttributeType=N \
    --key-schema AttributeName=user_id,KeyType=HASH AttributeName=update_ver,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
