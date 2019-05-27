from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re

""" rank_func
@ count : user가 그 product를 몇번 샀는지 누적한 횟수 테이블
@ favor_product : count 순서를 매김 제일 많이 구매한제품은 값 1
@ 등수만 필요하므로 count column은 drop하고 리턴
"""

def rank_func():

    # data from RDS -----------------------------------------------
    db = pymysql.connect(host="", port= , user="",passwd ="", db="")
    
    SQL = "SELECT order_id, user_id FROM orders"
    orders_df = pd.read_sql(SQL, db)
    del SQL
    
    SQL = "SELECT order_id, product_id FROM order_products__prior"
    prior_df = pd.read_sql(SQL,db)
    del SQL
    # -------------------------------------------------------------
    
 
    #merge
    prior_and_orders =pd.merge(prior_df, orders_df, how='inner', on=['order_id'])
    
    count = pd.DataFrame({'count' : prior_and_orders.groupby(["user_id", "product_id"]).size()}).reset_index()
    count['favor_product']=count.groupby('user_id')['count'].rank(method='min',ascending=0)
    prior_and_orders2=pd.merge(prior_and_orders, count, how='inner')
    return prior_and_orders2.drop(['count'], axis=1)

""" prod_order_rank_func
@ 상품에 관련된 피처, 유저아이디 필요없음
@ 데이터로 이용할때 상품아이디로 머지(상품아이디가 중복돼도 랭크 같음) -> 처음 온 사람들한테 추천해주기 좋음
@ 1번째로 카트에 담긴 제품들의 순위를 구하기 위한 데이터프레임 oder_series
@ 카트에 담긴 순서가 1인게 많으면 1
@ 카트에 담긴 순서 중 1이 없으면 나머지 제품중에 rank하게 됨
"""

def prod_order_rank_func():
    
    prior_df = pd.read_csv("instacart-market-basket-analysis/order_products__prior.csv", usecols = ["product_id","add_to_cart_order"])
    
    order_series=pd.DataFrame({'count' : prior_df.groupby([ "product_id","add_to_cart_order"]).size()}).reset_index()
    order_series['prod_rank']=order_series.groupby('add_to_cart_order')['count'].rank(method='min',ascending=0)
    order_series_rank=pd.concat([order_series], axis=1).loc[:,["add_to_cart_order","product_id","prod_rank"]]
    prior_and_orders2=pd.merge(prior_df, order_series_rank, how='inner')
    return prior_and_orders2
