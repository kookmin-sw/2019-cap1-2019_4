import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('Recommendation')
    
    response = table.get_item(
        Key={
            'user_id':  event['user_id'],
            'update_ver': 1
        }
    )
    
    print(response['Item'])
    
    return response['Item']
