import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import csv
import pickle
import xgboost as xgb

orders_df = pd.read_csv("orders.csv")
products_df = pd.read_csv("products.csv")
prior = pd.read_csv("order_products__prior.csv")

order_prior =pd.merge(prior, orders_df, how='inner', on=['order_id'])
order_prior_product = pd.merge(order_prior, products_df, how='inner', on=['product_id'])


## 특정단어는 organic으로 지정 : 유기농 상품을 찾는다.
order_prior_product['organic'] = order_prior_product.product_name.str.lower().str.contains('organic')

organic_sum = pd.DataFrame({'organic_pro': order_prior_product.groupby(['user_id','organic']).size()})
organic_prob = organic_sum/organic_sum.groupby(level=0).sum()
organic_prob.reset_index(inplace=True)

## 이후 필요한 테이블에 merge는 선택
# pd.merge("테이블 이름", organic_prob, how='inner', on=['organic', 'user_id'])
