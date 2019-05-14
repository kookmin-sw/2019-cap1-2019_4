from __future__ import print_function # Python 2/3 compatibility
import boto3
import pandas as pd
import MySQLdb
import sys

def add_item(table, user_id, product_id):
    table.put_item(
        Item={
        'user_id': user_id,
        'update_ver' : 1,
        'product_id': product_id
        }
    )


def main():

    # variable to connect to DB
    db = MySQLdb.connect(host="flexadsdb.cklcaxnrw3b0.us-east-2.rds.amazonaws.com",# host
                     user="wldud8463",         # username
                     passwd="dbswldud8!",  # password
                     db="Flex_ads")   # RDS database name

    # data which stores recommendation info
    recommendation = pd.read_csv(sys.argv[1] + ".csv")

    # get data from RDS, to show additional info to users
    product = pd.read_sql('SELECT product_id,product_name,aisle_id  FROM products', con=db)
    aisle= pd.read_sql('SELECT * FROM aisles', con=db)

    # columns in RDS  data
    print(product.columns)
    print(aisle.columns)

    # print a part of recommendation info
    #print(recommendation[0:30])

    print(type(recommendation.loc[0]['product_id']))
    print(type(product.loc[0]['product_id']))


    # remove rows if it takes no recommended product
    recommendation = recommendation[recommendation.product_id!="None"]

    # to merge data, change to the same data type
    recommendation['product_id'].apply(int)
    recommendation['product_id']=recommendation['product_id'].astype(int)

    # result data to store in DB
    result = pd.merge(recommendation, product, how='inner', on=['product_id'])
    result = pd.merge(result, aisle, how='inner', on=['aisle_id'])

    # print a part of result data to check
    print(result.head())

    # connect to dynamodb
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    # select table to add item
    table = dynamodb.Table('Recommendation')


    # add items to dynamoDB
    for i in range(result.shape[0]):
        print(i)
        add_item(table, result.loc[i]['user_id'], result.loc[i]['product_id'])

if __name__ == "__main__":
    main()

