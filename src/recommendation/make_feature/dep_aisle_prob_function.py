import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import csv
import pickle
import xgboost as xgb

# data
train = pd.read_csv("order_products__train.csv")
prior = pd.read_csv("order_products__prior.csv")
orders_df = pd.read_csv("orders.csv")
products_df = pd.read_csv("products.csv")
aisles_df = pd.read_csv("aisles.csv")
departments_df = pd.read_csv("departments.csv")
submit = pd.read_csv("sample_submission.csv")

order_prior =pd.merge(prior, orders_df, how='inner', on=['order_id'])
order_prior_product = pd.merge(order_prior, products_df, how='inner', on=['product_id'])

# nan값은 0으로 변경
order_prior_product = order_prior_product.fillna(0)
order_prior_product

""" department probability function
@ order_prior_product : order, prior, product data를 merge한 table
@ n_reorder: 재구매 기록의 수
@ reorder_dep : department별 재구매 수를 표현한 series
@ df_re_dep : reorder_dep의 dataframe화
@ dic : department와 department의 확률을 표현한 series
@ df_ : dic의 dataframe화
@ dep_prob_table : order_prior_product와 df_를 merge한 것
"""

def dep_prob (order_prior_product):
    reorder=order_prior_product.loc[order_prior_product['reordered']==1]
    #reorder

    n_reorder = len(reorder)
    #n_reorder

    reorder_dep = reorder.department_id.value_counts()

    df_re_dep = pd.DataFrame(reorder_dep)
    #df_re_dep

    dic = {"department_id": df_re_dep.index, "prob":(df_re_dep["department_id"]/n_reorder)}
    df_ = pd.DataFrame(dic)
    #df_

    dep_prob_table = pd.merge(order_prior_product, df_, how='inner', on=['department_id'])

    return dep_prob_table.head(5)


""" aisle probability function
@ order_prior_product : order, prior, product data를 merge한 table
@ n_reorder: 재구매 기록의 수
@ reorder_aisle : aisle별 재구매 수를 표현한 series
@ df_re_aisle : reorder_aisle의 dataframe화
@ dic : aisle와 aisle의 확률을 표현한 series
@ df_ : dic의 dataframe화
@ aisle_prob_table : order_prior_product와 df_를 merge한 것
"""
def aisle_prob(order_prior_product):
    reorder=order_prior_product.loc[order_prior_product['reordered']==1]
    #reorder

    n_reorder = len(reorder)
    #n_reorder

    reorder_aisle = reorder.aisle_id.value_counts()

    df_re_aisle = pd.DataFrame(reorder_aisle)
    #df_re_dep

    dic = {"aisle_id": df_re_aisle.index, "prob":(df_re_aisle["aisle_id"]/n_reorder)}
    df_ = pd.DataFrame(dic)
    #df_

    aisle_prob_table = pd.merge(order_prior_product, df_, how='inner', on=['aisle_id'])

    return aisle_prob_table.head(5)


""" dow probability function
@ order_prior_product : order, prior, product data를 merge한 table
@ n_reorder: 재구매 기록의 수
@ reorder_dow : dow별 재구매 수를 표현한 series
@ df_re_dow : reorder_dow의 dataframe화
@ dic : dow와 dow의 확률을 표현한 series
@ df_ : dic의 dataframe화
@ dow_prob_table : order_prior_product와 df_를 merge한 것
"""
def dow_prob(order_prior_product):
    reorder=order_prior_product.loc[order_prior_product['reordered']==1]
    #reorder

    n_reorder = len(reorder)
    #n_reorder

    reorder_dow = reorder.order_dow.value_counts()

    df_re_dow = pd.DataFrame(reorder_dow)
    #df_re_dep

    dic = {"order_dow": df_re_dow.index, "prob":(df_re_dow["order_dow"]/n_reorder)}
    df_ = pd.DataFrame(dic)
    #df_

    dow_prob_table = pd.merge(order_prior_product, df_, how='inner', on=['order_dow'])

    return (dow_prob_table.head(5))


dep_prob(order_prior_product)
aisle_prob(order_prior_product)
dow_prob(order_prior_product)
