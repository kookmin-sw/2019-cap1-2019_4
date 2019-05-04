# simple code to add item to db

from __future__ import print_function # Python 2/3 compatibility
import boto3
import pandas as pd

def add_item(table, user_id, product_id):
    table.put_item(
        Item={
        'user_id': user_id,
        'update_ver' : 1,
        'product_id': product_id
        }
    )


def main():
    # connect to dynamodb
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    # select table to add item
    table = dynamodb.Table('Recommendation')
    # the file which contains items
    recommendation = pd.read_csv("./xgboost_submission.csv")
   
    # add all item iteratively
    for i in range(recommendation.shape[0]):
        add_item(table, recommendation.loc[i]['user_id'], recommendation.loc[i]['product_id'])

if __name__ == "__main__":
    main()
