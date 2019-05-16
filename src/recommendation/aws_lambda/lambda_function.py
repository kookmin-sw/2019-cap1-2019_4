import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('Recommendation')
    
    user = event['user_id']
    print("User is comming, user_id is "),
    print(user)
    response = table.get_item(
        Key={
            'user_id' : user,
            'update_ver': 1
        }
    )
    print("recommend products(ads): "),
    
    # return information to show
    return (response['Item'])
