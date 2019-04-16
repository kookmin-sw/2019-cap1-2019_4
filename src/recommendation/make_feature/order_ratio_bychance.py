from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re

data_aisles = pd.read_csv("instacart-market-basket-analysis/aisles.csv")
data_departments = pd.read_csv("instacart-market-basket-analysis/departments.csv")
data_orders = pd.read_csv("instacart-market-basket-analysis/orders.csv")
data_product = pd.read_csv("instacart-market-basket-analysis/products.csv")
data_order_prior = pd.read_csv("instacart-market-basket-analysis/order_products__prior.csv")
data_order_train = pd.read_csv("instacart-market-basket-analysis/order_products__train.csv")

order_prior =pd.merge(data_order_prior, data_orders, how='inner', on=['order_id'])

"""order_ratio_bychance() 유저가 특정 product_id를 처음 샀을때와 마지막 샀을때의 기간동안 방문해서 구매한 비율을 나타냄
예를 들어 1번 product_id를 order_id( 5,6,8 ) 에 구매를 함 --> 5~8 order_id 기간동안 3번 구매함 --> 결과 3/(8-5+1)=3/4

@ cnt : user_id가 product_id를 구매한 총량
@ user_onb_max(onb_max) : user_id가 product_id를 마지막으로 구매한 order_number 값
@ user_item_min(onb_min) : user_id가 product_id를 처음 구매한 order_number 값
@ chance : user_id가 product_id를 구매한 order_number 구간의 길이(max-min+1)
@ chance 계산 마지막에 +1 한 이유는 예문에서 보이듯이 5~8구간은 4이지만 8-5하면 3이 출력돼서..+1
@order_ratio_bychance : cnt/chance 값으로 user_id가 product_id를 chance 기간동안 구매한 비율
"""
def order_ratio_bychance(order_prior):
    
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
    return prior_and_orders2.drop(['cnt','onb_max','onb_min','chance'], axis=1)

