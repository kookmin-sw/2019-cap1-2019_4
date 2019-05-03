from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re
"""
order_number_rev
@user에 관한것 머지는 user_id로
@order_number_rev : order_number.max - order_number
현재부터 마지막 order_number까지 남은 order_number

**다른함수에서 쓰는 변수이기때문에 가장먼저 실행해야 함**
"""

def order_number_rev() :
    
    orders_df = pd.read_csv("instacart-market-basket-analysis/orders.csv", usecols=["order_id","user_id","order_number"])
    prior_df = pd.read_csv("instacart-market-basket-analysis/order_products__prior.csv", usecols = ["order_id","add_to_cart_order"])
    
    #merge
    order_prior= pd.merge(prior_df, orders_df, how='inner', on=['order_id'])
    
    order_prior.sort_values(['order_id', 'add_to_cart_order'], inplace=True)
    order_prior.reset_index(drop=1, inplace=True)
    order_prior['order_number_rev'] =order_prior.groupby('user_id').order_number.transform(np.max) - order_prior.order_number
    
    return order_prior.drop(['add_to_cart_order','order_number'], axis=1)




