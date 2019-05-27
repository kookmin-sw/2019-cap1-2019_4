# basic feature : 대분류, 소분류, 요일, 시간에 대한 구매 확률
# ex : 대분류 육류의 재구매 확률 = 육류의 재구매 기록의 수(reordered=1) / 육류의 구매 기록수(reordered=0,1)

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import csv
import pickle
import xgboost as xgb
import pymysql


# data from RDS
db = pymysql.connect(host="", port= , user="",passwd ="", db="")

SQL = "SELECT * FROM orders"
orders_df = pd.read_sql(SQL, db)
del SQL

SQL = "SELECT * FROM order_products__prior"
prior = pd.read_sql(SQL,db)
del SQL

SQL = "SELECT * FROM products"
products_df pd.read_sql(SQL, db)
del SQL

order_prior =pd.merge(prior, orders_df, how='inner', on=['order_id'])
order_prior_product = pd.merge(order_prior, products_df, how='inner', on=['product_id'])

# nan값은 0으로 변경
order_prior_product = order_prior_product.fillna(0)


""" department probability function
@ order_prior_product : order, prior, product data를 merge한 table
@ count : department를 기준으로 재구매 기록의 수와 아닌 것의 수를 count라는 새로운 colunm에 기록한 table
@ temp : count의 series version
@ dep_prob : department를 기준으로 재구매 된 비율과 그렇지 않은 기록의 확률을 구한 table
                    ex : 육류의 재구매 기록 수 / 육류의 총 구매 기록 수 = 육류(특정 대분류)가 재구매 될 확률
@ tmp2 : dep_prob에서 reordered가 1인 행만 뽑아서 기록한 table
@ dep_prob_table : multi-index에 있는 index를 column으로 보낸 tmp2와 처음 파라미터로 들어온 table을 merge한 것
                   department_id별 재구매 확률이 새롭게 포함됨
"""

def dep_prob (order_prior_product):
    count = pd.DataFrame({'count' : order_prior_product.groupby(["department_id","reordered"]).size()}).reset_index()
    temp = count.groupby(['department_id', 'reordered'])['count'].sum().rename('dep_prob')
    dep_prob =(temp /temp.groupby(level=0).sum())

    # 재구매 된 것의 확률만 필요함 => reordered가 1인 것
    tmp2 = pd.DataFrame(dep_prob).xs(1,level='reordered')
    tmp2.reset_index(inplace=True)
    dep_prob_table = pd.merge(order_prior_product, tmp2, how='inner', on=['department_id'])
    return dep_prob_table

""" aisle probability function
@ order_prior_product : order, prior, product data를 merge한 table
@ count : aisle를 기준으로 재구매 기록의 수와 아닌 것의 수를 count라는 새로운 colunm에 기록한 table
@ temp : count의 series version
@ aisle_prob : aisle를 기준으로 재구매 된 비율과 그렇지 않은 기록의 확률을 구한 table
                    ex : 탄산음료류의 재구매 기록 수 / 탄산음료류의 총 구매 기록 수 = 탄산음료(특정 소분류)가 재구매 될 확률
@ tmp2 : aisle_prob에서 reordered가 1인 행만 뽑아서 기록한 table
@ aisle_prob_table : multi-index에 있는 index를 column으로 보낸 tmp2와 처음 파라미터로 들어온 table을 merge한 것
                   aisle_id별 재구매 확률이 새롭게 포함됨
"""

def aisle_prob(order_prior_product):
    count = pd.DataFrame({'count' : order_prior_product.groupby(["aisle_id","reordered"]).size()}).reset_index()
    temp = count.groupby(['aisle_id', 'reordered'])['count'].sum().rename('aisle_prob')
    aisle_prob =(temp /temp.groupby(level=0).sum())

    # 재구매 된 것의 확률만 필요함 => reordered가 1인 것
    tmp2 = pd.DataFrame(aisle_prob).xs(1,level='reordered')
    tmp2.reset_index(inplace=True)
    aisle_prob_table = pd.merge(order_prior_product, tmp2, how='inner', on=['aisle_id'])
    return aisle_prob_table


""" dow probability function
@ order_prior_product : order, prior, product data를 merge한 table
@ count : order_dow를 기준으로 재구매 기록의 수와 아닌 것의 수를 count라는 새로운 colunm에 기록한 table
@ temp : count의 series version
@ dow_prob : order_dow를 기준으로 재구매 된 비율과 그렇지 않은 기록의 확률을 구한 table
                    ex : 월요일의 재구매 기록 수 / 월요일의 총 구매 기록 수 = 월요일의 재구매 확률
@ tmp2 : dow_prob에서 reordered가 1인 행만 뽑아서 기록한 table
@ dow_prob_table : multi-index에 있는 index를 column으로 보낸 tmp2와 처음 파라미터로 들어온 table을 merge한 것
                   order_dow별 재구매 확률이 새롭게 포함됨
"""

def dow_prob(order_prior_product):
    count = pd.DataFrame({'count' : order_prior_product.groupby(["order_dow","reordered"]).size()}).reset_index()
    temp = count.groupby(['order_dow', 'reordered'])['count'].sum().rename('dow_prob')
    dow_prob =(temp /temp.groupby(level=0).sum())

    # 재구매 된 것의 확률만 필요함 => reordered가 1인 것
    tmp2 = pd.DataFrame(dow_prob).xs(1,level='reordered')
    tmp2.reset_index(inplace=True)
    dow_prob_table = pd.merge(order_prior_product, tmp2, how='inner', on=['order_dow'])
    return dow_prob_table


""" hour probability function
@ order_prior_product : order, prior, product data를 merge한 table
@ count : order_hour_of_day를 기준으로 재구매 기록의 수와 아닌 것의 수를 count라는 새로운 colunm에 기록한 table
@ temp : count의 series version
@ hour_prob : order_hour_of_day를 기준으로 재구매 된 비율과 그렇지 않은 기록의 확률을 구한 table
                    ex : 월요일의 재구매 기록 수 / 월요일의 총 구매 기록 수 = 월요일의 재구매 확률
@ tmp2 : hour_prob에서 reordered가 1인 행만 뽑아서 기록한 table
@ hour_prob_table : multi-index에 있는 index를 column으로 보낸 tmp2와 처음 파라미터로 들어온 table을 merge한 것
                   order_hour_of_day별 재구매 확률이 새롭게 포함됨
"""

def hour_prob(order_prior_product):
    count = pd.DataFrame({'count' : order_prior_product.groupby(["order_hour_of_day","reordered"]).size()}).reset_index()
    temp = count.groupby(['order_hour_of_day', 'reordered'])['count'].sum().rename('hour_prob')
    hor_prob =(temp /temp.groupby(level=0).sum())

    # 재구매 된 것의 확률만 필요함 => reordered가 1인 것
    tmp2 = pd.DataFrame(hour_prob).xs(1,level='reordered')
    tmp2.reset_index(inplace=True)
    hour_prob_table = pd.merge(order_prior_product, tmp2, how='inner', on=['order_hour_of_day'])
    return hour_prob_table
