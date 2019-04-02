# simple code to add item to db

from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('Recommendation')

print(table.creation_date_time)

table.put_item(
   Item={
        'user_id': 124,
        'update_ver': 1,
        'product_id': 24,
        'product_name' : 'banana'
    }
)
