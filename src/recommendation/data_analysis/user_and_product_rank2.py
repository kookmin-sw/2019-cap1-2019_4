from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re

data_aisles = pd.read_csv("../../../../instacart-market-basket-analysis/aisles.csv")
data_departments = pd.read_csv("../../../../instacart-market-basket-analysis/departments.csv")
data_orders = pd.read_csv("../../../../instacart-market-basket-analysis/orders.csv")
data_product = pd.read_csv("../../../../instacart-market-basket-analysis/products.csv")
data_order_prior = pd.read_csv("../../../../instacart-market-basket-analysis/order_products__prior.csv")
data_order_train = pd.read_csv("../../../../instacart-market-basket-analysis/order_products__train.csv")

order_prior =pd.merge(data_order_prior, data_orders, how='inner', on=['order_id'])

order_prior.head()

""" rank_func
@ count : user가 그 product를 몇번 샀는지 누적한 횟수 테이블
@ favor_product : count 순서를 매김 제일 많이 구매한제품은 값 1
@ 등수만 필요하므로 count column은 drop하고 리턴
"""
def rank_func(prior_and_orders):

    count = pd.DataFrame({'count' : prior_and_orders.groupby(["user_id", "product_id"]).size()}).reset_index()
    count['favor_product']=count.groupby('user_id')['count'].rank(method='min',ascending=0)
    #count_rank=pd.concat([count], axis=1).loc[:,["user_id","product_id","favor_product"]]
    prior_and_orders2=pd.merge(prior_and_orders, count, how='inner')
    return prior_and_orders2.drop(['count'], axis=1)


print(rank_func(order_prior).head())


""" prod_order_rank_func
@ 1번째로 카트에 담긴 제품들의 순위를 구하기 위한 데이터프레임 oder_series
@ 카트에 담긴 순서가 1인게 많으면 1
@ 카트에 담긴 순서 중 1이 없으면 나머지 제품중에 rank하게 됨
"""

def prod_order_rank_func(prior_and_orders):
    order_series=pd.DataFrame({'count' : prior_and_orders.groupby([ "product_id","add_to_cart_order"]).size()}).reset_index()
    order_series['prod_rank']=order_series.groupby('add_to_cart_order')['count'].rank(method='min',ascending=0)
    order_series_rank=pd.concat([order_series], axis=1).loc[:,["add_to_cart_order","product_id","prod_rank"]]
    prior_and_orders2=pd.merge(prior_and_orders, order_series_rank, how='inner')
    return prior_and_orders2

prod=prod_order_rank_func(rank_func(order_prior))

print(prod.head())

