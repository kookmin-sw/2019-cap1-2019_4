# coding: utf-8
'''
feature list
- order_number_rev()
- dep_prob()
- aisle_prob()
- dow_prob()
- hour_prob()
- organic_prob()
- latest_order()
- model()
'''

import pymysql
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import xgboost as xgb
from numpy import loadtxt
from xgboost import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree


###################### DB connect
db = pymysql.connect(host="", port=3306, user="", passwd="",db="")



### 상품, 유저 아이디로 뼈대와 결합
def order_ratio_bychance():
    
    ## 주문 정보가 있는 테이블에서 불러 올 것
    SQL = "SELECT order_id, user_id, order_number FROM orders"
    orders_df = pd.read_sql(SQL, db)
  
    ## 회원의 구매 내역에서 불러 올 것
    SQL = "SELECT order_id, product_id FROM order_products__prior"
    prior_df = pd.read_sql(SQL, db)

    #merge
    order_prior =pd.merge(prior_df, orders_df, how='inner', on=['order_id'])

    cnt =order_prior.groupby(['user_id', 'product_id']).size()
    cnt.name = 'cnt'
    cnt = cnt.reset_index()

    user_onb_max = order_prior.groupby('user_id').order_number.max().reset_index()
    user_onb_max.columns = ['user_id', 'onb_max']

    user_item_min = order_prior.groupby(['user_id', 'product_id']).order_number.min().reset_index()
    user_item_min.columns = ['user_id', 'product_id', 'onb_min']

    chance = pd.merge(user_item_min, user_onb_max, on='user_id', how='left')
    chance['chance'] = chance.onb_max - chance.onb_min +1

    df = pd.merge(cnt, chance, on=['user_id', 'product_id'], how='left')

    df['order_ratio_bychance'] = df.cnt / df.chance

    prior_and_orders2=pd.merge(order_prior, df, how='inner')
    result = prior_and_orders2.drop(['cnt','onb_max','onb_min','chance','order_id','order_number'], axis=1)
    del prior_and_orders2
    return result
