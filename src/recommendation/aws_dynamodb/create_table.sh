# create table in Dynamodb
aws dynamodb create-table \
    --table-name Recommendation \
    --attribute-definitions \
        AttributeName=user_id,AttributeType=N \ # Partition Key
        AttributeName=update_ver,AttributeType=N \  #Sort Key
    --key-schema AttributeName=user_id,KeyType=HASH AttributeName=update_ver,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
