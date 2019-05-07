#!/usr/bin/env python
# coding: utf-8

# In[10]:


from pandas import DataFrame
import pandas as pd
import json
import csv
import numpy as np
import re
import order_number_rev


# In[13]:


"""timezone()
@ time => order_hour_of_day 가 있는 데이터
@ 구매 시간을 midnight,morning,noon,night 4가지로 구분

@ 다른함수에서 쓰는 변수이기때문에 가장먼저 실행해야 함
"""

def timezone() :
    
    time = pd.read_csv("instacart-market-basket-analysis/orders.csv", usecols=["order_hour_of_day"])
    
    time.sort_values('order_hour_of_day', inplace=True)
    time.drop_duplicates(inplace=True)
    time.reset_index(drop=True, inplace=True)

    def timezone(s):
        if s < 6:
            #return 'midnight'
            return 0;
        elif s < 12:
            #return 'morning'
            return 1;
        elif s < 18:
            #return 'noon'
            return 2;
        else:
            #return 'night'
            return 3;

    time['timezone'] = time.order_hour_of_day.map(timezone)
    
    return time


# In[ ]:




