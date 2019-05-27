from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re
import order_number_rev

"""
mean_cart_num()
user_id별로 특정 product_id가 cart에 담기는 순서의 평균,최대,최소,중위값(ex:10개의 데이터가있으면 5번째 데이터),표준편차
prod_order_rank_func와 유사함

"""

def mean_cart_num() :
    
    db = pymysql.connect(host="", port= , user="",passwd ="", db="")

    SQL = "SELECT * FROM orders"
    orders_df = pd.read_sql(SQL, db)
    del SQL

    SQL = "SELECT * FROM order_products__prior"
    prior = pd.read_sql(SQL,db)
    del SQL
    
    #merge
    order_prior =pd.merge(prior, orders_df, how='inner', on=['order_id'])
    
    gr = order_prior.groupby(['user_id', 'product_id'])
    
    user = round(gr.add_to_cart_order.mean().to_frame(),3)
    user.columns = ['useritem_mean_cart']
    user['useritem_min_cart'] = gr.add_to_cart_order.min()
    user['useritem_median_cart'] = gr.add_to_cart_order.median()
    user['useritem_max_cart'] = gr.add_to_cart_order.max()
    user['useritem_std_cart'] = round(gr.add_to_cart_order.std(),3)
    user.reset_index(inplace=True)
    
    user=pd.merge(order_prior , user , on=['user_id','product_id'], how='left')
    return user



