from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re
import order_number_rev

"""
co_occur

@order_tbl : order_id를 size계산을 통해 'order_size'변수를 만듦

@tbl : user_id + product_id 기준 order_size의 값을 이용하여 아래 값들을 만듦
- useritem_cooccur-min , useritem_cooccur-max , useritem_cooccur-mean , useritem_cooccur-median , useritem_cooccur-std

@user_osz : order_tbl의 user_id별 order_size를 만든 값을 이용하여 min,max값을 찾음
- user_order_size-min , user_order_size-max

@tbl : user_osz( user_id별 order_size값 )과 tbl( user_id+product_id 별 order_size값)을 이용하여 아래의 값들을 만듦
- useritem_cooccur-min-min , useritem_cooccur-max-min , useritem_coocuur-max-max


"""



def co_occur() :
    db = pymysql.connect(host="", port= , user="", passwd="", db="")
    
    SQL = "SELECT * FROM orders"
    orders_df = pd.read_sql(SQL, db)
    del SQL

    SQL = "SELECT * FROM order_products__prior"
    prior = pd.read_sql(SQL,db)
    del SQL
    
    order_prior =pd.merge(or1, or2, how='inner', on=['order_id'])
    
    order_tbl= order_prior.groupby('order_id').size().to_frame()
    order_tbl.columns = ['order_size']
    order_tbl.reset_index(inplace=True)

    order_tbl = pd.merge(order_tbl, order_prior[['order_id', 'user_id', 'product_id']])
    
    col = ['user_id', 'product_id']
    tbl = order_prior.sort_values(col).drop_duplicates(col)[col]
    tbl = tbl.set_index(col)

    gr = order_tbl.groupby(['user_id', 'product_id'])

    tbl['useritem_cooccur-min'] = gr.order_size.min()
    tbl['useritem_cooccur-max'] = gr.order_size.max()
    tbl['useritem_cooccur-mean'] = gr.order_size.mean()
    tbl['useritem_cooccur-median'] = gr.order_size.median()
    tbl['useritem_cooccur-std'] = gr.order_size.std()
    tbl.reset_index(inplace=True)
    
    user_osz = order_tbl.groupby(['user_id']).order_size.min().to_frame()
    user_osz.columns = ['user_order_size-min']
    user_osz['user_order_size-max'] = order_tbl.groupby(['user_id']).order_size.max()
    user_osz.reset_index(inplace=True)
    
    tbl = pd.merge(tbl, user_osz, on='user_id', how='left')
    
    tbl['useritem_cooccur-min-min'] = tbl['user_order_size-min']  - tbl['useritem_cooccur-min']
    tbl['useritem_cooccur-max-min'] = tbl['useritem_cooccur-max'] - tbl['useritem_cooccur-min']
    tbl['useritem_cooccur-max-max'] = tbl['user_order_size-max'] - tbl['useritem_cooccur-max']
    tbl.drop(['user_order_size-min', 'user_order_size-max'], axis=1, inplace=True)
    
    return tbl

