
# coding: utf-8

# # 각 유저의 구매기록으로 대분류, 소분류, 요일, 시간별 구매 확률


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import csv
import pickle
import xgboost as xgb


'''
유저별로 구매 기록을 보고 구매된 대분류 확률을 구하는 함수. 
각 유저가 어떤 대분류에 대해 살 확률이 높은지 확인
@ dep_sum : 유저의 기록중 포함된 대분류별 기록의 수를 구한다.
@ dep_prob : 대분류별 확률을 구한 값이 포함된 table
'''
def dep_prob():

    orders_df = pd.read_csv("orders.csv", usecols=["order_id","user_id"])
    prior_df = pd.read_csv("order_products__prior.csv", usecols = ["order_id", "product_id"])
    products_df = pd.read_csv("products.csv", usecols = ["product_id", "department_id"])
    
    #merge
    order_prior =pd.merge(prior_df, orders_df, how='inner', on=['order_id'])
    order_prior_product = pd.merge(order_prior, products_df, how='inner', on=['product_id'])
    order_prior_product
    
    del orders_df, prior_df, products_df
    
    # 유저를 기준으로 각 대분류 개수 구하기
    dep_sum = pd.DataFrame({'user_dep_prob': order_prior_product.groupby(['user_id','department_id']).size()})
    
    # 대분류의 구매수를 유저의 총 구매수로 나눈다.
    dep_prob = dep_sum/dep_sum.groupby(level=0).sum()
    
    # change index to column
    dep_prob.reset_index(inplace=True)  
    
    del dep_sum, order_prior_product
    
    return dep_prob

'''
유저별로 구매 기록을 보고 구매된 소분류 확률을 구하는 함수. 
각 유저가 어떤 소분류에대해 살 확률이 높은지 확인
@ aisle_sum : 유저의 기록중 포함된 소분류별 기록의 수를 구한다.
@ aisle_prob : 소분류별 확률을 구한 값이 포함된 table
'''
def aisle_prob():

    orders_df = pd.read_csv("orders.csv", usecols=["order_id","user_id"])
    prior_df = pd.read_csv("order_products__prior.csv", usecols = ["order_id", "product_id"])
    products_df = pd.read_csv("products.csv", usecols = ["product_id", "aisle_id"])
    
    #merge
    order_prior =pd.merge(prior_df, orders_df, how='inner', on=['order_id'])
    order_prior_product = pd.merge(order_prior, products_df, how='inner', on=['product_id'])
    order_prior_product
    
    del orders_df, prior_df, products_df
    
    # 유저를 기준으로 각 대분류 개수 구하기
    aisle_sum = pd.DataFrame({'user_aisle_prob': order_prior_product.groupby(['user_id','aisle_id']).size()})
    
    # 대분류의 구매수를 유저의 총 구매수로 나눈다.
    aisle_prob = aisle_sum/aisle_sum.groupby(level=0).sum()
    
    # change index to column
    aisle_prob.reset_index(inplace=True)  
    
    del aisle_sum, order_prior_product
    
    return aisle_prob

'''
유저별로 구매 기록을 보고 요일별 확률을 구하는 함수. 
각 유저가 어떤 요일에 살 확률이 높은지 확인
@ dow_sum : 유저의 기록중 포함된 요일 기록의 수를 구한다.
@ dow_prob : 요일 확률을 구한 값이 포함된 table
'''
def dow_prob():

    orders_df = pd.read_csv("orders.csv", usecols=["order_id","user_id","order_dow"])
    prior_df = pd.read_csv("order_products__prior.csv", usecols = ["order_id", "product_id"])
    products_df = pd.read_csv("products.csv", usecols = ["product_id"])
    
    #merge
    order_prior =pd.merge(prior_df, orders_df, how='inner', on=['order_id'])
    order_prior_product = pd.merge(order_prior, products_df, how='inner', on=['product_id'])
    order_prior_product
    
    del orders_df, prior_df, products_df
    
    # 유저를 기준으로 각 대분류 개수 구하기
    dow_sum = pd.DataFrame({'user_dow_prob': order_prior_product.groupby(['user_id','order_dow']).size()})
    
    # 대분류의 구매수를 유저의 총 구매수로 나눈다.
    dow_prob = dow_sum/dow_sum.groupby(level=0).sum()
    
    # change index to column
    dow_prob.reset_index(inplace=True)  
    
    del dow_sum, order_prior_product
    
    return dow_prob

'''
유저별로 구매 기록을 보고 시간의 구매 확률을 구하는 함수. 
각 유저가 어떤 시간에대해 살 확률이 높은지 확인
@ hour_sum : 유저의 기록중 포함된 시간별 기록의 수를 구한다.
@ hor_prob : 시간별 확률을 구한 값이 포함된 table
'''

def hour_prob():

    orders_df = pd.read_csv("orders.csv", usecols=["order_id","user_id","order_hour_of_day"])
    prior_df = pd.read_csv("order_products__prior.csv", usecols = ["order_id", "product_id"])
    products_df = pd.read_csv("products.csv", usecols = ["product_id"])
    
    #merge
    order_prior =pd.merge(prior_df, orders_df, how='inner', on=['order_id'])
    order_prior_product = pd.merge(order_prior, products_df, how='inner', on=['product_id'])
    order_prior_product
    
    del orders_df, prior_df, products_df
    
    # 유저를 기준으로 각 대분류 개수 구하기
    hour_sum = pd.DataFrame({'user_hour_prob': order_prior_product.groupby(['user_id','order_hour_of_day']).size()})
    
    # 대분류의 구매수를 유저의 총 구매수로 나눈다.
    hour_prob = hour_sum/hour_sum.groupby(level=0).sum()
    
    # change index to column
    hour_prob.reset_index(inplace=True)  
    
    del hour_sum, order_prior_product
    
    return hour_prob




