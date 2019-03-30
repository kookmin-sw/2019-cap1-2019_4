
# coding: utf-8

# # 각 유저의 구매기록으로 대분류, 소분류, 요일, 시간별 구매 확률
# 

# In[2]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import csv
import pickle
import xgboost as xgb


# In[90]:


# data

train = pd.read_csv("order_products__train.csv")
prior = pd.read_csv("order_products__prior.csv")
orders_df = pd.read_csv("orders.csv")
products_df = pd.read_csv("products.csv")
aisles_df = pd.read_csv("aisles.csv")
departments_df = pd.read_csv("departments.csv")
submit = pd.read_csv("sample_submission.csv")


# In[94]:


# 필요한 데이터 merge

order_prior =pd.merge(prior, orders_df, how='inner', on=['order_id'])
order_prior_product = pd.merge(order_prior, products_df, how='inner', on=['product_id'])
#order_prior_product


# In[88]:


'''
유저별로 구매 기록을 보고 구매된 대분류 확률을 구하는 함수. 
각 유저가 어떤 대분류에 대해 살 확률이 높은지 확인
@ dep_sum : 유저의 기록중 포함된 대분류별 기록의 수를 구한다.
@ dep_prob : 대분류별 확률을 구한 값이 포함된 table
'''
def dep_prob_per_user(order_prior_product):    
    # 유저를 기준으로 대분류의 개수 구하기
    dep_sum = pd.DataFrame({'user_dep_prob': order_prior_product.groupby(['user_id','department_id']).size()})
    
    # 유저를 기준으로 구매기록 수
    # A.groupby(level=0).sum()
    
    # 대분류의 구매수를 유저의 총 구매수로 나눈다.
    dep_prob = A/A.groupby(level=0).sum()
    
    # change index to column
    dep_prob.reset_index(inplace=True)  
    
    # 원래 큰 table과 merge하기 : 기준은 사용자와 대분류 2개를 동시에 기준으로! 
    dep_per_user = pd.merge(order_prior_product, dep_prob, how='inner', on=['user_id', 'department_id'])
    return dep_per_user


# In[91]:


'''
유저별로 구매 기록을 보고 구매된 소분류 확률을 구하는 함수. 
각 유저가 어떤 소분류에대해 살 확률이 높은지 확인
@ aisle_sum : 유저의 기록중 포함된 소분류별 기록의 수를 구한다.
@ aisle_prob : 소분류별 확률을 구한 값이 포함된 table
'''
def aisle_prob_per_user(order_prior_product):    
    # 유저를 기준으로 대분류의 개수 구하기
    aisle_sum = pd.DataFrame({'user_aisle_prob': order_prior_product.groupby(['user_id','aisle_id']).size()})
    
    # 대분류의 구매수를 유저의 총 구매수로 나눈다.
    aisle_prob = A/A.groupby(level=0).sum()
    
    # change index to column
    aisle_prob.reset_index(inplace=True)  
    
    # 원래 큰 table과 merge하기 : 기준은 사용자와 대분류 2개를 동시에 기준으로! 
    aisle_per_user = pd.merge(order_prior_product, aisle_prob, how='inner', on=['user_id', 'aisle_id'])
    return aisle_per_user


# In[92]:


'''
유저별로 구매 기록을 보고 요일별 확률을 구하는 함수. 
각 유저가 어떤 요일에 살 확률이 높은지 확인
@ dow_sum : 유저의 기록중 포함된 요일 기록의 수를 구한다.
@ dow_prob : 요일 확률을 구한 값이 포함된 table
'''
def dow_prob_per_user(order_prior_product):    
    # 유저를 기준으로 대분류의 개수 구하기
    dow_sum = pd.DataFrame({'user_dow_prob': order_prior_product.groupby(['user_id','order_dow']).size()})

    # 대분류의 구매수를 유저의 총 구매수로 나눈다.
    dow_prob = A/A.groupby(level=0).sum()
    
    # change index to column
    dow_prob.reset_index(inplace=True)  
    
    # 원래 큰 table과 merge하기 : 기준은 사용자와 대분류 2개를 동시에 기준으로! 
    dow_per_user = pd.merge(order_prior_product, dow_prob, how='inner', on=['user_id', 'order_dow'])
    return dow_per_user


# In[93]:


'''
유저별로 구매 기록을 보고 시간의 구매 확률을 구하는 함수. 
각 유저가 어떤 시간에대해 살 확률이 높은지 확인
@ hour_sum : 유저의 기록중 포함된 시간별 기록의 수를 구한다.
@ hor_prob : 시간별 확률을 구한 값이 포함된 table
'''
def hour_prob_per_user(order_prior_product):    
    # 유저를 기준으로 대분류의 개수 구하기
    hour_sum = pd.DataFrame({'user_hour_prob': order_prior_product.groupby(['user_id','order_hour']).size()})

    # 대분류의 구매수를 유저의 총 구매수로 나눈다.
    hour_prob = A/A.groupby(level=0).sum()
    
    # change index to column
    hour_prob.reset_index(inplace=True)  
    
    # 원래 큰 table과 merge하기 : 기준은 사용자와 대분류 2개를 동시에 기준으로! 
    hour_per_user = pd.merge(order_prior_product, hour_prob, how='inner', on=['user_id', 'order_hour'])
    return hour_per_user


# In[ ]:




