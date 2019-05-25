from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re
import order_number_rev

"""
days_since_fitst_order()
@days_since_first_order : user_id기준 첫 구매부터 지난 days
 - 계산방법 : days_since_prior_order의 누적 합산
 
**다른함수에서 쓰는 변수이고, order_number_rev를 사용하기 때문에 order_number_rev 바로 뒤에 실행해야 함**
"""
def days_since_first_order() :
    temp = order_number_rev()
    # data from RDS
    db = pymysql.connect(host="", port= , user="",passwd ="", db="")
    SQL = "SELECT * FROM orders"
    orders_df = pd.read_sql(SQL, db)
    del SQL

    order_prior = pd.merge(temp, order_df, how='inner', on=['user_id'])
    
    order_prior.sort_values(['user_id', 'order_number'],inplace=True)
    order_prior.reset_index(drop=1, inplace=True)
    order_prior.order_number_rev = order_prior.order_number_rev.fillna(-1).astype(int)
    order_prior['days_since_first_order'] = order_prior.groupby('user_id').days_since_prior_order.cumsum()
    
    return order_prior

