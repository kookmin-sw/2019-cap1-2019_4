from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re

"""dow_prod 요일별로 많이 팔린 product rank
@ count : 해당 product가 요일별로 구매된 횟수
@ dow_rank : 요일별로 많이 구매된 prouduct 순위. 순위가 높으면 1.
@ 등수만 필요하므로 count coulmn은 drop하고 리턴
"""
def dow_prod():
    
    orders_df = pd.read_csv("instacart-market-basket-analysis/orders.csv", usecols=["order_id","order_dow"])
    prior_df = pd.read_csv("instacart-market-basket-analysis/order_products__prior.csv", usecols = ["order_id", "product_id"])
    
    #merge
    prior_and_orders = pd.merge(prior_df, orders_df, how='inner', on=['order_id'])
    
    order_series=pd.DataFrame({'count' : prior_and_orders.groupby([ "order_dow","product_id"]).size()}).reset_index()
    order_series['dow_rank']=order_series.groupby('order_dow')['count'].rank(method='min',ascending=0)
    prior_and_orders2=pd.merge(prior_and_orders, order_series, how='inner')
    return prior_and_orders2.drop(['count'], axis=1)


"""prod_count() 상품별 팔린 개수를 알려주는 함수
@ prod_count : 해당 product가 총 구매된 개수
"""
def prod_count():
    
    prior_and_orders = pd.read_csv("instacart-market-basket-analysis/order_products__prior.csv", usecols = ["product_id"])
    
    order_series=pd.DataFrame({'prod_count' : prior_and_orders.groupby(["product_id"]).size()}).reset_index()
    prior_and_orders2=pd.merge(prior_and_orders, order_series, how='inner')
    return prior_and_orders2


