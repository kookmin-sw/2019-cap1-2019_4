from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re
import order_number_rev

"""
together()
-> 상품에 관한 피처, 머지는 상품아이디로
order_id 별로 구입총량을 계산하여
특정 product_id를 구입할때 한번에 구매하는 product 종류(총량) 의 mean,min,max,std
@item_together_mean : 평균값
@item_together_min : 최솟값
@item_together_max :  최댓값
@item_together_std : 표준편차

"""
def together():

    order_prior = pd.read_csv("instacart-market-basket-analysis/order_products__prior.csv", usecols = ["order_id", "product_id"])

    order_size = order_prior.groupby('order_id').size().reset_index()
    order_size.columns = ['order_id', 'total']
    order_prior_ = pd.merge(order_prior, order_size, on='order_id', how='left')
    
    item = order_prior_.groupby('product_id').total.mean().to_frame()
    item.columns = ['item_together_mean']
    
    item['item_together_min'] =order_prior_.groupby('product_id').total.min()
    item['item_together_max'] = order_prior_.groupby('product_id').total.max()
    item['item_together_std'] =order_prior_.groupby('product_id').total.std()
    
    order_prior_=pd.merge( order_prior_ , item , on=['product_id'] , how='left')
    return order_prior_
