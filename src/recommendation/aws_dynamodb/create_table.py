# create Recommedation table using python

from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')


table = dynamodb.create_table(
    TableName='Recommendation',
    KeySchema=[
        {
            'AttributeName': 'user_id',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'update_ver',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_id',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'update_ver',
            'AttributeType': 'N'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

print("Table status:", table.table_status)
