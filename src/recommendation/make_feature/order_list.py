from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re
import order_number_rev

""" od_reordered()
@ 각 order_id에서 구매된 product_id를 나열하는 함수.
"""
def od_reordered():
    
    db = pymysql.connect(host="", port= , user="",passwd ="", db="")
    
    SQL = "SELECT * FROM order_products__prior"
    log = pd.read_sql(SQL,db)
    del SQL
    
    log_ = log.loc[log.reordered==1]
    order_reorderd = log_.groupby('order_id').product_id.apply(list).reset_index()
    return order_reordered


